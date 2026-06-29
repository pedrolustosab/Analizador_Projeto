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
            'tag_cls': tag_cls, 'bar_cls': bar_cls,
            # NOVOS CAMPOS FINANCEIROS PARA O DRILLDOWN DA TABELA EVA
            'bac': r['bac'], 'pv': r['pv'], 'ev': r['ev'], 'ac': r['ac'],
            'sv': r['ev'] - r['pv'], 'cv': r['ev'] - r['ac'],
            'spi': r['ev'] / r['pv'] if r['pv'] > 0 else 1.0,
            'cpi': r['ev'] / r['ac'] if r['ac'] > 0 else 1.0
        })

    max_money = max(bac, eac) * 1.1
    if max_money <= 0: max_money = 1

    def g_x(d): return 80 + ((d - min_date).days / tot_days) * 1100
    def g_y(v): return 340 - (v / max_money) * 320

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

    return {
        "proj_name": proj_name, "status_date": status_date.strftime('%d/%m/%y'),
        "tot_tasks": len(df), "b_end": df['b_end'].max().strftime('%d/%m/%y'), "f_end": df['end'].max().strftime('%d/%m/%y'),
        "sv_days": (df['end'].max() - df['b_end'].max()).days, "late_count": len(df[df['status'] == 'Atrasada']),
        "pct_phys": (df['pct'].mean()) if len(df)>0 else 0, "pct_fin": (ac/bac*100) if bac>0 else 0, "pct_done": (len(df[df['status'] == 'Concluída'])/len(df)*100) if len(df)>0 else 0,
        "spi": spi, "cpi": cpi, "bac": bac, "pv": pv, "ev": ev, "ac": ac, "eac": eac, "vac": bac - eac, "sv": ev - pv, "cv": ev - ac,
        "has_finance": has_finance,
        "today_pct": f"{today_pct:.2f}%", "tasks": tasks_out,
        "chart": {
            "pv_pts": " ".join(pv_pts), "ev_pts": " ".join(ev_pts), "ac_pts": " ".join(ac_pts), 
            "fc_ev": fc_ev_pts, "fc_ac": fc_ac_pts, 
            "tx": today_x, "m": max_money,
            "max_y_labels": [0, max_money*0.25, max_money*0.5, max_money*0.75, max_money]
        }
    }