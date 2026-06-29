import pandas as pd
import xml.etree.ElementTree as ET
import io

def parse_xml_to_json(file_bytes):
    tree = ET.parse(io.BytesIO(file_bytes))
    root = tree.getroot()
    ns = root.tag.split('}')[0] + '}' if '}' in root.tag else ''
    
    proj_name = root.find(f'.//{ns}Title')
    proj_name = proj_name.text if proj_name is not None else "Projeto Executivo"
    
    sd_node = root.find(f'.//{ns}StatusDate')
    status_date = pd.to_datetime(sd_node.text).tz_localize(None) if sd_node is not None else pd.Timestamp.now()

    resources = {res.find(f'{ns}UID').text: res.find(f'{ns}Name').text 
                 for res in root.findall(f'.//{ns}Resource') 
                 if res.find(f'{ns}UID') is not None and res.find(f'{ns}Name') is not None and res.find(f'{ns}Name').text}

    assignments = {}
    for ass in root.findall(f'.//{ns}Assignment'):
        t_uid, r_uid = ass.find(f'{ns}TaskUID'), ass.find(f'{ns}ResourceUID')
        if t_uid is not None and r_uid is not None and r_uid.text in resources:
            assignments.setdefault(t_uid.text, []).append(resources[r_uid.text])
                
    tasks_raw = []
    for seq, task in enumerate(root.findall(f'.//{ns}Task')):
        uid = task.find(f'{ns}UID')
        name = task.find(f'{ns}Name')
        if uid is None or name is None or not name.text: continue
        
        id_node = task.find(f'{ns}ID')
        try:
            row_id = int(id_node.text)
        except:
            row_id = seq

        # ORDENAÇÃO INFALÍVEL: Extrai a estrutura analítica (WBS/OutlineNumber)
        out_node = task.find(f'{ns}OutlineNumber')
        out_str = out_node.text if out_node is not None and out_node.text else ""
        
        try:
            # Transforma "1.2.10" em uma tupla matemática (1, 2, 10) para ordenação perfeita
            wbs_tuple = tuple(int(x) for x in out_str.split('.') if x.isdigit())
        except:
            wbs_tuple = ()
            
        if not wbs_tuple:
            wbs_tuple = (999999, seq) # Se não tiver WBS, joga pro final
        
        start, finish = task.find(f'{ns}Start'), task.find(f'{ns}Finish')
        b_start, b_finish = task.find(f'.//{ns}Baseline/{ns}Start'), task.find(f'.//{ns}Baseline/{ns}Finish')
        pct = task.find(f'{ns}PercentComplete')
        lvl = task.find(f'{ns}OutlineLevel')
        milestone = task.find(f'{ns}Milestone')
        
        cost, ac_node = task.find(f'{ns}Cost'), task.find(f'{ns}ActualCost')
        b_cost = task.find(f'.//{ns}Baseline/{ns}Cost')
        
        cost_val = float(cost.text) if cost is not None and cost.text else 0.0
        b_cost_val = float(b_cost.text) if b_cost is not None and b_cost.text else cost_val
        
        tasks_raw.append({
            'wbs_tuple': wbs_tuple,
            'id': row_id,
            'uid': uid.text, 'name': name.text,
            'start': pd.to_datetime(start.text[:10]) if start is not None and start.text else None,
            'end': pd.to_datetime(finish.text[:10]) if finish is not None and finish.text else None,
            'b_start': pd.to_datetime(b_start.text[:10]) if b_start is not None and b_start.text else None,
            'b_end': pd.to_datetime(b_finish.text[:10]) if b_finish is not None and b_finish.text else None,
            'pct': float(pct.text) if pct is not None and pct.text else 0.0,
            'level': int(lvl.text) if lvl is not None and lvl.text else 1,
            'isMilestone': True if milestone is not None and milestone.text == '1' else False,
            'bac': b_cost_val, 'ac': float(ac_node.text) if ac_node is not None and ac_node.text else 0.0,
            'owner': ", ".join(assignments.get(uid.text, ["Equipe"]))
        })
        
    df = pd.DataFrame(tasks_raw).dropna(subset=['start', 'end'])
    if df.empty: return {}
    
    # ORDENA PELA WBS (1 -> 1.1 -> 1.2 -> 2 -> 2.1) E DEPOIS PELO ID
    df = df.sort_values(['wbs_tuple', 'id'])
    
    df['b_start'] = df['b_start'].fillna(df['start'])
    df['b_end'] = df['b_end'].fillna(df['end'])
    
    df['parent'] = ""
    last_uids = {}
    for idx, row in df.iterrows():
        lvl = row['level']
        if lvl > 1 and (lvl - 1) in last_uids:
            df.at[idx, 'parent'] = last_uids[lvl - 1]
        last_uids[lvl] = row['uid']
        
    parent_counts = df['parent'].value_counts().to_dict()
    df['children'] = df['uid'].map(lambda x: parent_counts.get(x, 0))

    df['sv_days'] = (df['end'] - df['b_end']).dt.days
    df['status'] = "No Prazo"
    df.loc[df['pct'] == 100, 'status'] = "Concluída"
    df.loc[(df['pct'] < 100) & ((df['sv_days'] > 0) | (df['end'] < status_date)), 'status'] = "Atrasada"

    def calc_pv(x):
        if x['b_end'] <= status_date: return x['bac']
        if x['b_start'] <= status_date:
            return x['bac'] * ((status_date - x['b_start']).days / max(1, (x['b_end'] - x['b_start']).days))
        return 0.0

    df['pv'] = df.apply(calc_pv, axis=1)
    df['ev'] = df['bac'] * (df['pct'] / 100)
    
    lvl1 = df[df['level'] == 1] if not df[df['level'] == 1].empty else df
    bac, pv, ev, ac = lvl1['bac'].sum(), lvl1['pv'].sum(), lvl1['ev'].sum(), lvl1['ac'].sum()
    
    has_finance = bac > 0
    
    spi = ev / pv if pv > 0 else 1.0
    cpi = ev / ac if ac > 0 else 1.0
    eac = bac / cpi if cpi > 0 else bac

    min_date = df[['start', 'b_start']].min().min()
    max_date = df[['end', 'b_end']].max().max()
    tot_days = (max_date - min_date).days
    if tot_days <= 0: tot_days = 1
    today_pct = max(0, min(100, (status_date - min_date).days / tot_days * 100))

    tasks_out = []
    for _, r in df.iterrows():
        b_l = max(0, (r['b_start'] - min_date).days / tot_days * 100)
        b_w = max(0.5, (r['b_end'] - r['b_start']).days / tot_days * 100)
        a_l = max(0, (r['start'] - min_date).days / tot_days * 100)
        a_w = max(0.5, (r['end'] - r['start']).days / tot_days * 100)
        
        tag_cls = 'done' if r['status'] == 'Concluída' else ('late-tag' if r['status'] == 'Atrasada' else 'planned')
        bar_cls = 'donebar' if r['status'] == 'Concluída' else ('late' if r['status'] == 'Atrasada' else 'cur')
        if r['children'] > 0 and r['pct'] < 100: bar_cls = 'phase'
        if r['isMilestone']: bar_cls += ' milestone'

        tasks_out.append({
            'uid': r['uid'], 'parent': r['parent'], 'children': r['children'], 'name': r['name'], 'owner': r['owner'],
            'pct': int(r['pct']), 'start': r['start'].strftime('%d/%m/%Y'), 'finish': r['end'].strftime('%d/%m/%Y'),
            'b_start': r['b_start'].strftime('%d/%m/%Y'), 'b_finish': r['b_end'].strftime('%d/%m/%Y'),
            'svd': r['sv_days'], 'status': r['status'], 'level': r['level'],
            'b_left': f"{b_l:.2f}%", 'b_width': f"{b_w:.2f}%", 'a_left': f"{a_l:.2f}%", 'a_width': f"{a_w:.2f}%",
            'tag_cls': tag_cls, 'bar_cls': bar_cls
        })

    max_money = max(bac, eac) * 1.1
    if max_money <= 0: max_money = 1

    def g_x(d): return 80 + ((d - min_date).days / tot_days) * 1100
    def g_y(v): return 340 - (v / max_money) * 320

    # O gráfico financeiro é ordenado por data
    df_c = df[df['level'] > 1].sort_values('b_end')
    pv_pts, ev_pts, ac_pts = [f"{g_x(min_date):.1f},340"], [f"{g_x(min_date):.1f},340"], [f"{g_x(min_date):.1f},340"]
    c_pv = c_ev = c_ac = 0

    for _, r in df_c.iterrows():
        c_pv += r['bac']
        pv_pts.append(f"{g_x(r['b_end']):.1f},{g_y(c_pv):.1f}")
        if r['end'] <= status_date:
            c_ev += r['ev']; c_ac += r['ac']
            ev_pts.append(f"{g_x(r['end']):.1f},{g_y(c_ev):.1f}")
            ac_pts.append(f"{g_x(r['end']):.1f},{g_y(c_ac):.1f}")

    today_x, end_x = g_x(status_date), g_x(max_date)
    fc_ev_pts = f"{today_x:.1f},{g_y(c_ev):.1f} {end_x:.1f},{g_y(bac):.1f}"
    fc_ac_pts = f"{today_x:.1f},{g_y(c_ac):.1f} {end_x:.1f},{g_y(eac):.1f}"

    phases = []
    if has_finance:
        for _, r in df[df['level'] == 1].iterrows():
            phases.append({'name': r['name'], 'bac': r['bac'], 'pv': r['pv'], 'ev': r['ev'], 'ac': r['ac'], 'sv': r['ev']-r['pv'], 'cv': r['ev']-r['ac'], 'spi': r['ev']/r['pv'] if r['pv']>0 else 1.0, 'cpi': r['ev']/r['ac'] if r['ac']>0 else 1.0})

    return {
        "proj_name": proj_name, "status_date": status_date.strftime('%d/%m/%y'),
        "tot_tasks": len(df), "b_end": df['b_end'].max().strftime('%d/%m/%y'), "f_end": df['end'].max().strftime('%d/%m/%y'),
        "sv_days": (df['end'].max() - df['b_end'].max()).days, "late_count": len(df[df['status'] == 'Atrasada']),
        "pct_phys": (df['pct'].mean()) if len(df)>0 else 0, "pct_fin": (ac/bac*100) if bac>0 else 0, "pct_done": (len(df[df['status'] == 'Concluída'])/len(df)*100) if len(df)>0 else 0,
        "spi": spi, "cpi": cpi, "bac": bac, "pv": pv, "ev": ev, "ac": ac, "eac": eac, "vac": bac - eac, "sv": ev - pv, "cv": ev - ac,
        "has_finance": has_finance,
        "today_pct": f"{today_pct:.2f}%", "tasks": tasks_out, "phases": phases,
        "chart": {
            "pv_pts": " ".join(pv_pts), "ev_pts": " ".join(ev_pts), "ac_pts": " ".join(ac_pts), 
            "fc_ev": fc_ev_pts, "fc_ac": fc_ac_pts, 
            "tx": today_x, "m": max_money,
            "max_y_labels": [0, max_money*0.25, max_money*0.5, max_money*0.75, max_money]
        }
    }