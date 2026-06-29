import json

def get_html_template(d):
    fmt = lambda x: f"R$ {x/1000:,.1f}k".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    gantt_html = ""
    for t in d['tasks']:
        pad = (t['level'] - 1) * 18
        hidden = "hidden" if t['parent'] else ""
        late_val = "1" if t['status'] == 'Atrasada' else "0"
        toggle = f"<span class='toggle' id='tg-{t['uid']}'>+</span>" if t['children'] > 0 else f"<span class='toggle dot'></span>"
        fw = "fw-bold" if t['children'] > 0 else ""
        sv_str = f"+{t['svd']}d" if t['svd'] > 0 else f"{t['svd']}d"

        gantt_html += f"""
        <div class='gantt-row {hidden}' data-uid='{t['uid']}' data-parent='{t['parent']}' data-late='{late_val}'>
            <div class='task' style='padding-left:{pad}px' onclick='toggleOrDetail("{t['uid']}")'>
                {toggle}<span class='t-name {fw}'>{t['name']}</span>
                <div class='meta'>{t['owner']} · BL {t['b_finish'][:5]} · Atual {t['finish'][:5]} · SV {sv_str} <span class='tag {t['tag_cls']}'>{t['status']}</span></div>
            </div>
            <div class='linebox' onclick='showDetail("{t['uid']}")'>
                <span class='today' style='left:{d['today_pct']}'></span>
                <span class='base' style='left:{t['b_left']};width:{t['b_width']}'></span>
                <span class='bar {t['bar_cls']}' style='left:{t['a_left']};width:{t['a_width']}'></span>
            </div>
            <div class='pct'>{t['pct']}%</div>
        </div>"""

    # Lógica do Tracker (Timeline)
    tracker_html = ""
    for m in d['milestones']:
        tracker_html += f"""
        <li class="step {m['state']}">
            <div class="node"></div>
            <p>{m['name']}</p>
            <small>{m['date']}</small>
        </li>
        """
    if not tracker_html:
        tracker_html = "<li class='step pending'><p>Nenhum marco cadastrado</p></li>"

    if d['has_finance']:
        spi_str = f"{d['spi']:.2f}"
        cpi_str = f"{d['cpi']:.2f}"
        pct_fin_str = f"{d['pct_fin']:.1f}%"
        fin_warn_bar = "warnbar" if d['pct_fin'] > d['pct_phys'] else ""
        fin_bar_width = f"{d['pct_fin']}%"
        
        eva_rows_html = ""
        for t in d['tasks']:
            pad = (t['level'] - 1) * 20
            hidden = "hidden" if t['parent'] else ""
            toggle = f"<span class='toggle' id='tg-eva-{t['uid']}'>+</span>" if t['children'] > 0 else f"<span class='toggle dot'></span>"
            fw = "fw-bold" if t['children'] > 0 else ""
            
            eva_rows_html += f"""
            <tr class='eva-row {hidden}' data-uid='{t['uid']}' data-parent='{t['parent']}'>
                <td style='padding-left:{pad + 34}px; cursor:pointer;' onclick='togglePhase("{t['uid']}")'>
                    <div style='position:relative;'>{toggle}<span class='{fw}'>{t['name']}</span></div>
                </td>
                <td>{fmt(t['bac'])}</td><td>{fmt(t['pv'])}</td><td>{fmt(t['ev'])}</td><td>{fmt(t['ac'])}</td>
                <td class='{'pos' if t['sv']>=0 else 'neg'}'>{fmt(t['sv'])}</td><td class='{'pos' if t['cv']>=0 else 'neg'}'>{fmt(t['cv'])}</td>
                <td class='{'pos' if t['spi']>=1 else 'neg'}'>{t['spi']:.2f}</td><td class='{'pos' if t['cpi']>=1 else 'neg'}'>{t['cpi']:.2f}</td>
            </tr>"""

        eva_content = f"""
            <div class='eva-grid'>
                <div class='eva-card'><span>Budget (BAC)</span><b>{fmt(d['bac'])}</b></div>
                <div class='eva-card'><span>Planejado (PV)</span><b>{fmt(d['pv'])}</b></div>
                <div class='eva-card'><span>Agregado (EV)</span><b>{fmt(d['ev'])}</b></div>
                <div class='eva-card'><span>Realizado (AC)</span><b>{fmt(d['ac'])}</b></div>
                <div class='eva-card'><span>Var. Prazo (SV)</span><b class='{'pos' if d['sv']>=0 else 'neg'}'>{fmt(d['sv'])}</b></div>
                <div class='eva-card'><span>Var. Custo (CV)</span><b class='{'pos' if d['cv']>=0 else 'neg'}'>{fmt(d['cv'])}</b></div>
                <div class='eva-card'><span>SPI</span><b class='{'pos' if d['spi']>=1 else 'neg'}'>{d['spi']:.2f}</b></div>
                <div class='eva-card'><span>CPI</span><b class='{'pos' if d['cpi']>=1 else 'neg'}'>{d['cpi']:.2f}</b></div>
                <div class='eva-card'><span>EAC</span><b>{fmt(d['eac'])}</b></div>
                <div class='eva-card'><span>VAC</span><b class='{'pos' if d['vac']>=0 else 'neg'}'>{fmt(d['vac'])}</b></div>
            </div>
            
            <div class='svg-container'>
                <div style="overflow-x: auto;">
                    <svg viewBox="0 0 1200 380" style="width: 100%; min-width: 900px; font-family: Inter, sans-serif;">
                        <line x1="80" y1="340" x2="1180" y2="340" stroke="#f1f5f9" stroke-width="2"/>
                        <text x="70" y="344" text-anchor="end" fill="#94a3b8" font-size="12" font-weight="600">R$ 0</text>
                        <line x1="80" y1="260" x2="1180" y2="260" stroke="#f1f5f9" stroke-width="2"/><text x="70" y="264" text-anchor="end" fill="#94a3b8" font-size="12" font-weight="600">{fmt(d['chart']['max_y_labels'][1])}</text>
                        <line x1="80" y1="180" x2="1180" y2="180" stroke="#f1f5f9" stroke-width="2"/><text x="70" y="184" text-anchor="end" fill="#94a3b8" font-size="12" font-weight="600">{fmt(d['chart']['max_y_labels'][2])}</text>
                        <line x1="80" y1="100" x2="1180" y2="100" stroke="#f1f5f9" stroke-width="2"/><text x="70" y="104" text-anchor="end" fill="#94a3b8" font-size="12" font-weight="600">{fmt(d['chart']['max_y_labels'][3])}</text>
                        <line x1="{d['chart']['tx']:.1f}" y1="10" x2="{d['chart']['tx']:.1f}" y2="340" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="6"/>
                        
                        <polyline points="{d['chart']['pv_pts']}" fill="none" stroke="#94a3b8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                        <polyline points="{d['chart']['ev_pts']}" fill="none" stroke="#0ea5e9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                        <polyline points="{d['chart']['ac_pts']}" fill="none" stroke="#f43f5e" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                        <polyline points="{d['chart']['fc_ev']}" fill="none" stroke="#0ea5e9" stroke-width="3" stroke-dasharray="6" stroke-linecap="round"/>
                        <polyline points="{d['chart']['fc_ac']}" fill="none" stroke="#f43f5e" stroke-width="3" stroke-dasharray="6" stroke-linecap="round"/>
                    </svg>
                </div>
            </div>
            <div class='tw' style='margin-top:16px;'><table><thead><tr><th>Estrutura Analítica</th><th>BAC</th><th>PV</th><th>EV</th><th>AC</th><th>SV</th><th>CV</th><th>SPI</th><th>CPI</th></tr></thead><tbody>{eva_rows_html}</tbody></table></div>
        """
    else:
        spi_str, cpi_str, pct_fin_str, fin_warn_bar, fin_bar_width = "N/D", "N/D", "N/D", "", "0%"
        eva_content = "<div style='text-align:center; padding: 60px 20px; background:#f8fafc; border-radius:16px; border: 2px dashed #cbd5e1;'><h3>Análise Indisponível</h3></div>"

    tasks_json = json.dumps(d['tasks'], ensure_ascii=False)
    
    html = f"""<!DOCTYPE html><html lang='pt-BR'>
    <head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
        <style>
            :root{{--line:#e2e8f0;--ink:#0f172a;--muted:#64748b;--blue:#0ea5e9;--green:#10b981;--red:#f43f5e;}}
            *{{box-sizing:border-box; margin:0; padding:0; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;}}
            body{{background:#f8fafc;color:var(--ink); padding-bottom: 50px;}}
            .shell{{max-width:1440px;margin:0 auto;padding:0 24px;}}
            
            /* TRACKER DELIVERY APP STYLE */
            .tracker-container {{ background: #fff; padding: 40px 20px; border-radius: 20px; border: 1px solid var(--line); box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02); overflow-x: auto; margin-bottom: 24px; }}
            .tracker {{ display: flex; list-style: none; justify-content: space-between; position: relative; min-width: 800px; padding: 0 20px; }}
            
            .step {{ width: 100%; position: relative; text-align: center; z-index: 2; }}
            .step::after {{ content: ''; position: absolute; height: 4px; background: #e2e8f0; top: 12px; left: 50%; width: 100%; z-index: -1; }}
            .step:last-child::after {{ display: none; }}
            
            .node {{ width: 28px; height: 28px; background: #fff; border: 4px solid #cbd5e1; border-radius: 50%; margin: 0 auto 12px auto; transition: all 0.3s; }}
            .step p {{ font-size: 13px; font-weight: 700; color: #475569; line-height: 1.2; margin-bottom: 4px; }}
            .step small {{ font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase; }}
            
            /* States */
            .completed .node {{ background: var(--green); border-color: var(--green); }}
            .completed::after {{ background: var(--green); }}
            
            .active .node {{ background: var(--blue); border-color: #e0f2fe; box-shadow: 0 0 0 6px #e0f2fe; animation: pulse 2s infinite; }}
            .active p {{ color: var(--blue); }}
            
            .active-late .node {{ background: var(--red); border-color: #ffe4e6; box-shadow: 0 0 0 6px #ffe4e6; animation: pulseLate 2s infinite; }}
            .active-late p {{ color: var(--red); }}
            
            .late .node {{ background: var(--red); border-color: var(--red); }}
            .late::after {{ background: var(--red); }}
            
            @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.4); }} 70% {{ box-shadow: 0 0 0 10px rgba(14, 165, 233, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(14, 165, 233, 0); }} }}
            @keyframes pulseLate {{ 0% {{ box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.4); }} 70% {{ box-shadow: 0 0 0 10px rgba(244, 63, 94, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); }} }}

            /* GANTT & KPI STYLES (Enxutos) */
            .kpis,.eva-grid{{display:grid;grid-template-columns:repeat(5,1fr);gap:16px; margin-bottom:24px;}}
            .kpi,.eva-card{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:20px; text-align:center;}}
            .kpi span,.eva-card span{{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;font-weight:700;}}
            .kpi b,.eva-card b{{display:block;font-size:24px;font-weight:600;margin-top:8px; color: var(--ink);}}
            .gantt-row{{display:grid;grid-template-columns:520px 1fr 50px;gap:16px;align-items:center;min-width:900px;border-bottom:1px solid #f1f5f9;padding:12px 0;}}
            .gantt-row:hover{{background: #f8fafc;}}
            .task{{cursor:pointer; display:flex; flex-direction:column; position:relative;}}
            .toggle{{display:inline-flex;width:20px;height:20px;align-items:center;justify-content:center;border:1px solid #cbd5e1;border-radius:4px;background:#fff; font-weight:bold; position:absolute; left:-28px;}}
            .toggle.dot{{border:none; background:#cbd5e1; width:6px; height:6px; border-radius:50%; left:-21px; top:8px;}}
            .linebox{{position:relative;height:36px;background:#f8fafc;border-radius:8px;overflow:hidden; border:1px solid #e2e8f0;}}
            .today{{position:absolute;top:0;bottom:0;width:2px;background:#94a3b8;z-index:2;}}
            .base{{position:absolute;top:10px;height:4px;border-radius:99px;background:#cbd5e1;}}
            .bar{{position:absolute;top:18px;height:8px;border-radius:99px;}}
            .cur{{background:var(--blue);}}.donebar{{background:var(--green);}}.late{{background:var(--red);}}.phase{{background:#8b5cf6;}}
            .pct{{text-align:right;font-weight:700; font-size:13px;}}
            .hidden{{display:none!important;}}
            table{{width:100%;border-collapse:collapse;font-size:13px; background:#fff; border-radius:12px; overflow:hidden;}}
            th{{text-align:left;color:#64748b;font-size:11px;text-transform:uppercase;border-bottom:1px solid #cbd5e1;padding:12px 10px;}}
            td{{border-bottom:1px solid #f1f5f9;padding:12px 10px; cursor:pointer;}}
            .pos{{color:var(--green);}}.neg{{color:var(--red);}}
        </style>
    </head>
    <body><div class='shell'>
        
        <h2 style="margin: 24px 0 16px 0; font-size:20px;">Linha do Tempo (Marcos do Projeto)</h2>
        <div class="tracker-container">
            <ul class="tracker">
                {tracker_html}
            </ul>
        </div>
        
        <h2 style="margin: 32px 0 16px 0; font-size:20px;">Diagnóstico de Prazo</h2>
        <div class='kpis'>
            <div class='kpi'><span>Fim Planejado</span><b>{d['b_end']}</b></div>
            <div class='kpi'><span>Fim Projetado</span><b>{d['f_end']}</b></div>
            <div class='kpi'><span>Desvio de Prazo</span><b class='{"neg" if d['sv_days']>0 else "pos"}'>{f"+{d['sv_days']}" if d['sv_days']>0 else d['sv_days']} d</b></div>
            <div class='kpi'><span>Avanço Físico</span><b>{d['pct_phys']:.1f}%</b></div>
            <div class='kpi'><span>Avanço Financeiro</span><b>{pct_fin_str}</b></div>
        </div>

        <h2 style="margin: 32px 0 16px 0; font-size:20px;">Cronograma WBS (Gantt)</h2>
        <div style="background:#fff; padding:20px; border-radius:16px; border:1px solid #e2e8f0; overflow-x:auto;">
            {gantt_html}
        </div>

        <h2 style="margin: 32px 0 16px 0; font-size:20px;">Performance Financeira (EVM)</h2>
        {eva_content}
        
    </div>
    
    <script>
    const tasks = {tasks_json};
    const byUid = Object.fromEntries(tasks.map(t => [String(t.uid), t]));
    const expanded = new Set();
    tasks.filter(t=>t.children > 0).forEach(t=>expanded.add(String(t.uid))); // Auto-expand all on load
    
    function isAncestorExpanded(uid) {{
        let p = byUid[uid].parent;
        while (p && p !== "") {{
            if (!expanded.has(String(p))) return false;
            p = byUid[p].parent;
        }}
        return true;
    }}
    
    function toggleOrDetail(uid){{
        if(byUid[String(uid)].children > 0) togglePhase(uid);
    }}
    function togglePhase(uid){{
        const id = String(uid);
        if(expanded.has(id)) expanded.delete(id); else expanded.add(id);
        renderVisibility();
    }}
    
    function renderVisibility(){{
        document.querySelectorAll('.gantt-row, .eva-row').forEach(row => {{
            const uid = row.dataset.uid;
            const parentId = row.dataset.parent;
            if (!parentId || parentId === "") {{ row.classList.remove('hidden'); }} 
            else {{ row.classList.toggle('hidden', !isAncestorExpanded(uid)); }}
            
            if (byUid[uid].children > 0) {{
                const tgGantt = document.getElementById('tg-'+uid);
                const tgEva = document.getElementById('tg-eva-'+uid);
                const sign = expanded.has(uid) ? '−' : '+';
                if (tgGantt) tgGantt.textContent = sign;
                if (tgEva) tgEva.textContent = sign;
            }}
        }});
    }}
    renderVisibility();
    </script></body></html>"""
    return html