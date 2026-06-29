import json

def get_html_template(d):
    fmt = lambda x: f"R$ {x/1000:,.1f}k".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    # 1. Montagem das Linhas do Gantt (Completo e de Alta Qualidade)
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

    # 2. Montagem Tabela de Atrasos
    delays_html = ""
    lates = [t for t in d['tasks'] if t['status'] == 'Atrasada' and t['children'] == 0]
    lates.sort(key=lambda x: x['svd'], reverse=True)
    for t in lates:
        delays_html += f"<tr onclick='showDetail(\"{t['uid']}\")'><td>{t['uid']}</td><td>{t['name']}</td><td>{t['owner']}</td><td>{t['pct']}%</td><td>{t['b_finish'][:5]}</td><td>{t['finish'][:5]}</td><td class='neg'>+{t['svd']}d</td></tr>"
    if not delays_html: delays_html = "<tr><td colspan='7' style='text-align:center;'>Nenhuma tarefa folha em atraso no momento.</td></tr>"

    # 3. Lógica do Tracker de Marcos (Linha do Tempo Delivery)
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

    # 4. Lógica Financeira (Cards + Curva S SVG + Tabela Drilldown)
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
                <div class='eva-card'><span>Budget (BAC)</span><b>{fmt(d['bac'])}</b><small>Total Aprovado</small></div>
                <div class='eva-card'><span>Planejado (PV)</span><b>{fmt(d['pv'])}</b><small>Esforço Agendado</small></div>
                <div class='eva-card'><span>Agregado (EV)</span><b>{fmt(d['ev'])}</b><small>Entrega Realizada</small></div>
                <div class='eva-card'><span>Custo Real (AC)</span><b>{fmt(d['ac'])}</b><small>Gasto Incorrido</small></div>
                <div class='eva-card'><span>Var. Prazo (SV)</span><b class='{'pos' if d['sv']>=0 else 'neg'}'>{fmt(d['sv'])}</b><small>EV - PV</small></div>
                <div class='eva-card'><span>Var. Custo (CV)</span><b class='{'pos' if d['cv']>=0 else 'neg'}'>{fmt(d['cv'])}</b><small>EV - AC</small></div>
                <div class='eva-card'><span>SPI</span><b class='{'pos' if d['spi']>=1 else 'neg'}'>{d['spi']:.2f}</b><small>> 1.0 é positivo</small></div>
                <div class='eva-card'><span>CPI</span><b class='{'pos' if d['cpi']>=1 else 'neg'}'>{d['cpi']:.2f}</b><small>> 1.0 é positivo</small></div>
                <div class='eva-card'><span>EAC</span><b>{fmt(d['eac'])}</b><small>Custo projetado</small></div>
                <div class='eva-card'><span>VAC</span><b class='{'pos' if d['vac']>=0 else 'neg'}'>{fmt(d['vac'])}</b><small>BAC - EAC</small></div>
            </div>
            
            <div class='svg-container'>
                <div class="svg-legend">
                    <span><svg width="14" height="14"><rect width="14" height="14" fill="#94a3b8"/></svg> Valor Planejado (PV)</span>
                    <span><svg width="14" height="14"><rect width="14" height="14" fill="#0ea5e9"/></svg> Valor Agregado (EV)</span>
                    <span><svg width="14" height="14"><rect width="14" height="14" fill="#f43f5e"/></svg> Custo Real (AC)</span>
                    <span style="margin-left: 10px;"><svg width="24" height="4"><line x1="0" y1="2" x2="24" y2="2" stroke="#64748b" stroke-width="2" stroke-dasharray="4"/></svg> Forecast</span>
                </div>
                <div style="overflow-x: auto;">
                    <svg viewBox="0 0 1200 380" style="width: 100%; min-width: 900px; font-family: Inter, sans-serif;">
                        <line x1="80" y1="340" x2="1180" y2="340" stroke="#f1f5f9" stroke-width="2"/>
                        <text x="70" y="344" text-anchor="end" fill="#94a3b8" font-size="12" font-weight="600">R$ 0</text>
                        <line x1="80" y1="260" x2="1180" y2="260" stroke="#f1f5f9" stroke-width="2"/><text x="70" y="264" text-anchor="end" fill="#94a3b8" font-size="12" font-weight="600">{fmt(d['chart']['max_y_labels'][1])}</text>
                        <line x1="80" y1="180" x2="1180" y2="180" stroke="#f1f5f9" stroke-width="2"/><text x="70" y="184" text-anchor="end" fill="#94a3b8" font-size="12" font-weight="600">{fmt(d['chart']['max_y_labels'][2])}</text>
                        <line x1="80" y1="100" x2="1180" y2="100" stroke="#f1f5f9" stroke-width="2"/><text x="70" y="104" text-anchor="end" fill="#94a3b8" font-size="12" font-weight="600">{fmt(d['chart']['max_y_labels'][3])}</text>
                        <line x1="80" y1="20" x2="1180" y2="20" stroke="#f1f5f9" stroke-width="2"/><text x="70" y="24" text-anchor="end" fill="#94a3b8" font-size="12" font-weight="600">{fmt(d['chart']['max_y_labels'][4])}</text>
                        
                        <line x1="{d['chart']['tx']:.1f}" y1="10" x2="{d['chart']['tx']:.1f}" y2="340" stroke="#cbd5e1" stroke-width="2" stroke-dasharray="6"/>
                        <rect x="{d['chart']['tx'] - 30:.1f}" y="350" width="60" height="24" rx="4" fill="#f1f5f9"/>
                        <text x="{d['chart']['tx']:.1f}" y="366" text-anchor="middle" fill="#64748b" font-size="11" font-weight="700">HOJE</text>
                        
                        <polyline points="{d['chart']['pv_pts']}" fill="none" stroke="#94a3b8" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                        <polyline points="{d['chart']['ev_pts']}" fill="none" stroke="#0ea5e9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                        <polyline points="{d['chart']['ac_pts']}" fill="none" stroke="#f43f5e" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
                        <polyline points="{d['chart']['fc_ev']}" fill="none" stroke="#0ea5e9" stroke-width="3" stroke-dasharray="6" stroke-linecap="round"/>
                        <polyline points="{d['chart']['fc_ac']}" fill="none" stroke="#f43f5e" stroke-width="3" stroke-dasharray="6" stroke-linecap="round"/>
                        
                        <circle cx="1180" cy="{340 - (d['bac'] / d['chart']['m']) * 320:.1f}" r="5" fill="#0ea5e9" stroke="#fff" stroke-width="2"/>
                        <text x="1170" y="{340 - (d['bac'] / d['chart']['m']) * 320 - 12:.1f}" text-anchor="end" fill="#0ea5e9" font-size="12" font-weight="700">BAC {fmt(d['bac'])}</text>
                        <circle cx="1180" cy="{340 - (d['eac'] / d['chart']['m']) * 320:.1f}" r="5" fill="#f43f5e" stroke="#fff" stroke-width="2"/>
                        <text x="1170" y="{340 - (d['eac'] / d['chart']['m']) * 320 - 12:.1f}" text-anchor="end" fill="#f43f5e" font-size="12" font-weight="700">EAC {fmt(d['eac'])}</text>
                    </svg>
                </div>
            </div>
            
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:32px;">
                <h3 style="font-size:18px; color:#1e293b; margin:0;">Extrato Financeiro (WBS)</h3>
                <div><button onclick='expandAll()'>Expandir Tudo</button> <button onclick='collapseAll()'>Recolher Tudo</button></div>
            </div>
            <div class='tw' style='margin-top:16px;'><table><thead><tr><th>Estrutura Analítica</th><th>BAC</th><th>PV</th><th>EV</th><th>AC</th><th>SV</th><th>CV</th><th>SPI</th><th>CPI</th></tr></thead><tbody>{eva_rows_html}</tbody></table></div>
        """
    else:
        spi_str, cpi_str, pct_fin_str, fin_warn_bar, fin_bar_width = "N/D", "N/D", "N/D", "", "0%"
        eva_content = "<div style='text-align:center; padding: 60px 20px; background:#f8fafc; border-radius:16px; border: 2px dashed #cbd5e1; margin-top: 16px;'><h3 style='color:#334155;'>Análise Indisponível</h3></div>"

    tasks_json = json.dumps(d['tasks'], ensure_ascii=False)
    
    html = f"""<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
    <title>Premium XML Dashboard</title>
    <style>
        :root{{--line:#e2e8f0;--ink:#0f172a;--muted:#64748b;--red:#e11d48;--green:#059669;--amber:#ea580c; --blue:#0284c7; --blue-light:#0ea5e9;}}
        *{{box-sizing:border-box}}
        body{{margin:0;background:#f8fafc;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}}
        .shell{{max-width:1440px;margin:0 auto;padding:24px}}
        
        /* HEADER E NAV (Restaurados) */
        .hero{{display:grid;grid-template-columns:1.2fr .8fr;gap:20px;background:linear-gradient(135deg,#0f172a,#1e293b 56%,#334155);border-radius:24px;padding:32px;color:#fff;box-shadow:0 10px 25px rgba(15,23,42,.15)}}
        .hero h1{{margin:8px 0 8px;font-size:32px; letter-spacing: -0.5px;}}
        .eyebrow{{font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#cbd5e1;font-weight:700}}
        .hero p{{color:#94a3b8; font-size: 15px; margin-top: 0;}}
        .hero-panel{{background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.1);border-radius:16px;padding:20px}}
        .hero-grid{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}
        .hero-mini{{background:rgba(0,0,0,.2);border-radius:12px;padding:16px}}
        .hero-mini span{{display:block;font-size:11px;color:#94a3b8;text-transform:uppercase;font-weight:700}}
        .hero-mini b{{display:block;font-size:24px;margin-top:6px; color:#fff;}}
        .nav{{position:sticky;top:0;z-index:10;background:rgba(248,250,252,.9);backdrop-filter:blur(12px);padding:16px 0;margin:16px 0 0 0; display:flex; gap: 8px; align-items:center; border-bottom: 1px solid var(--line)}}
        .nav a,.nav button,button{{border:1px solid var(--line);background:#fff;border-radius:8px;padding:10px 16px;color:#334155;text-decoration:none;font-size:13px;font-weight:600;cursor:pointer; transition: 0.2s}}
        .nav a:hover, button:hover {{background: #f1f5f9; border-color: #cbd5e1;}}
        .section{{background:#fff;border:1px solid var(--line);border-radius:24px;padding:28px;margin-top:24px;box-shadow:0 4px 6px -1px rgba(0,0,0,.05)}}
        h2{{margin:0 0 20px 0;font-size:20px; letter-spacing: -0.5px; color: #1e293b;}}
        
        /* KPIS E PROGRESSO */
        .kpis,.eva-grid,.progress-grid{{display:grid;grid-template-columns:repeat(6,1fr);gap:16px}}
        .progress-grid{{grid-template-columns:repeat(3,1fr);margin-top:16px}}
        .kpi,.eva-card,.progress-card{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:20px; box-shadow: 0 1px 3px rgba(0,0,0,.03)}}
        .kpi span,.eva-card span,.progress-card span{{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;font-weight:700; letter-spacing: 0.5px;}}
        .kpi span{{text-align:center}}
        .kpi b{{display:block;text-align:center;font-size:32px;font-weight:600;margin-top:12px; color: var(--ink);}}
        .eva-card b,.progress-card b{{display:block;font-size:24px;font-weight:600;margin-top:10px; color: var(--ink);}}
        .kpi small,.eva-card small,.progress-card small{{display:block;margin-top:12px;color:#64748b;font-size:12px}}
        .bar-bg{{height:8px;background:#f1f5f9;border-radius:999px;overflow:hidden;margin-top:14px}}
        .bar-fill{{height:100%;border-radius:999px;background:var(--blue)}}
        .bar-fill.warnbar{{background:var(--amber)}}
        .neg{{color:var(--red)!important;font-weight:700}}.pos{{color:var(--green)!important;font-weight:700}}.warn{{color:var(--amber)!important;font-weight:700}}
        
        /* GANTT E TABELAS (Restaurados) */
        .gantt-tools{{display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap; margin-bottom: 20px;}}
        .gantt-tools input{{border:1px solid var(--line);border-radius:8px;padding:10px 16px;min-width:320px; font-size: 13px; outline: none;}}
        .gantt-tools input:focus{{border-color: var(--blue);}}
        .gantt,.tw{{overflow-x:auto}}
        .gantt-row{{display:grid;grid-template-columns:520px 1fr 68px;gap:16px;align-items:center;min-width:1000px;border-bottom:1px solid #f1f5f9;padding:12px 0;}}
        .gantt-row:hover{{background: #f8fafc;}}
        .hidden{{display:none!important}}
        .task{{cursor:pointer; display:flex; flex-direction:column; justify-content: center; position: relative;}}
        .fw-bold {{font-weight: 600; color: #1e293b;}}
        .t-name {{font-size: 14px;}}
        .toggle{{display:inline-flex;width:20px;height:20px;align-items:center;justify-content:center;border:1px solid #cbd5e1;border-radius:6px;background:#fff; font-size:14px; font-weight: bold; color: #475569; position:absolute; left: -28px; top: 0px;}}
        .toggle.dot{{border: none; background: #e2e8f0; width: 6px; height: 6px; border-radius: 50%; left: -16px; top: 7px;}}
        .meta{{font-size:12px;color:#64748b;margin-top:6px}}
        .linebox{{position:relative;height:36px;border:1px solid #e2e8f0;background:#f8fafc;border-radius:8px;overflow:hidden}}
        .today{{position:absolute;top:0;bottom:0;width:2px;background:#cbd5e1;z-index:2}}
        .base{{position:absolute;top:10px;height:4px;border-radius:99px;background:#cbd5e1}}
        .bar{{position:absolute;top:18px;height:8px;border-radius:99px}}
        .cur{{background:var(--blue-light)}}.donebar{{background:#10b981}}.late{{background:#f43f5e}}.phase{{background:#6366f1}}
        .bar.milestone{{height:12px!important;width:12px!important;top:12px!important;transform:rotate(45deg);border-radius:3px;background:#334155!important}}
        .pct{{text-align:right;font-weight:700; font-size:13px; color:#334155}}
        .tag{{display:inline-flex;border-radius:4px;padding:2px 6px;font-size:10px;font-weight:700; margin-left: 6px; letter-spacing: 0.5px;}}
        .done{{background:#d1fae5;color:#047857}}.planned{{background:#e0f2fe;color:#0369a1}}.late-tag{{background:#ffe4e6;color:#be123c}}
        table{{width:100%;border-collapse:collapse;font-size:13px}}
        th{{text-align:left;color:#64748b;font-size:11px;text-transform:uppercase;border-bottom:1px solid #cbd5e1;padding:12px 10px; font-weight: 700;}}
        td{{border-bottom:1px solid #f1f5f9;padding:12px 10px; color: #334155;}}
        tr:hover td{{background: #f8fafc;}}
        
        /* MODAL (Restaurado) */
        .modal-backdrop{{position:fixed;inset:0;background:rgba(15,23,42,.6);display:none;align-items:center;justify-content:center;padding:20px;z-index:99; backdrop-filter: blur(4px);}}
        .modal-backdrop.flex{{display:flex}}
        .modal{{background:white;max-width:800px;width:100%;border-radius:24px;padding:32px; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.25);}}
        .detail-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px; margin-top: 24px;}}
        .detail-box{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:16px}}
        .detail-label{{font-size:11px;text-transform:uppercase;font-weight:700;color:#64748b;}}
        .detail-value{{font-weight:700;margin-top:8px; font-size: 16px; color: #0f172a;}}
        .close{{float:right; background: #f1f5f9; color: #334155; border: none;}}
        
        /* SVG CHART */
        .svg-container {{ background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 24px; margin-top: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,.05); }}
        .svg-legend {{ display: flex; gap: 20px; margin-bottom: 24px; justify-content: center; font-size: 13px; font-weight: 600; color: #475569; }}
        
        /* TRACKER DE MARCOS (Injetado perfeitamente no layout premium) */
        .tracker-container {{ overflow-x: auto; padding: 20px 0; }}
        .tracker {{ display: flex; list-style: none; justify-content: space-between; position: relative; min-width: 800px; padding: 0 20px; margin: 0; }}
        .step {{ width: 100%; position: relative; text-align: center; z-index: 2; }}
        .step::after {{ content: ''; position: absolute; height: 4px; background: #e2e8f0; top: 12px; left: 50%; width: 100%; z-index: -1; }}
        .step:last-child::after {{ display: none; }}
        .node {{ width: 28px; height: 28px; background: #fff; border: 4px solid #cbd5e1; border-radius: 50%; margin: 0 auto 12px auto; transition: all 0.3s; }}
        .step p {{ font-size: 13px; font-weight: 700; color: #475569; line-height: 1.2; margin-bottom: 4px; }}
        .step small {{ font-size: 11px; color: #94a3b8; font-weight: 600; text-transform: uppercase; }}
        .completed .node {{ background: #10b981; border-color: #10b981; }}
        .completed::after {{ background: #10b981; }}
        .active .node {{ background: #0ea5e9; border-color: #e0f2fe; box-shadow: 0 0 0 6px #e0f2fe; animation: pulse 2s infinite; }}
        .active p {{ color: #0ea5e9; }}
        .active-late .node {{ background: #f43f5e; border-color: #ffe4e6; box-shadow: 0 0 0 6px #ffe4e6; animation: pulseLate 2s infinite; }}
        .active-late p {{ color: #f43f5e; }}
        .late .node {{ background: #f43f5e; border-color: #f43f5e; }}
        .late::after {{ background: #f43f5e; }}
        @keyframes pulse {{ 0% {{ box-shadow: 0 0 0 0 rgba(14, 165, 233, 0.4); }} 70% {{ box-shadow: 0 0 0 10px rgba(14, 165, 233, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(14, 165, 233, 0); }} }}
        @keyframes pulseLate {{ 0% {{ box-shadow: 0 0 0 0 rgba(244, 63, 94, 0.4); }} 70% {{ box-shadow: 0 0 0 10px rgba(244, 63, 94, 0); }} 100% {{ box-shadow: 0 0 0 0 rgba(244, 63, 94, 0); }} }}
    </style>
    </head>
    <body><div class='shell'>
        
        <header class='hero'>
            <div><div class='eyebrow'>Executive Dashboard</div><h1>{d['proj_name']}</h1>
            <p>Acompanhamento do seu projeto de forma fácil e inteligente.</p></div>
            <div class='hero-panel'><div class='hero-grid'>
                <div class='hero-mini'><span>Data Base</span><b>{d['status_date']}</b></div>
                <div class='hero-mini'><span>Tarefas Mapeadas</span><b>{d['tot_tasks']}</b></div>
                <div class='hero-mini'><span>Índice de Prazo (SPI)</span><b>{spi_str}</b></div>
                <div class='hero-mini'><span>Índice de Custo (CPI)</span><b>{cpi_str}</b></div>
            </div></div>
        </header>
        
        <nav class='nav'>
            <a href='#prazo'>Resumo do Projeto</a>
            <a href='#timeline'>Linha do Tempo</a>
            <a href='#gantt'>Gantt Interativo</a>
            <a href='#atrasos'>Painel de Atrasos</a>
            <a href='#eva'>Curva S & EVM</a>
        </nav>
        
        <section class='section' id='prazo'><h2>Diagnóstico de Cronograma</h2>
            <div class='kpis'>
                <div class='kpi'><span>Total de Atividades</span><b>{d['tot_tasks']}</b><small>Tarefas e Marcos</small></div>
                <div class='kpi'><span>Fim Planejado (BL)</span><b>{d['b_end']}</b><small>Linha de base original</small></div>
                <div class='kpi'><span>Fim Projetado</span><b>{d['f_end']}</b><small class='{"warn" if d['sv_days']>0 else ""}'>{f"+{d['sv_days']}" if d['sv_days']>0 else d['sv_days']} dias de desvio</small></div>
                <div class='kpi'><span>Em Atraso</span><b class='neg'>{d['late_count']}</b><small>Tarefas fora do prazo</small></div>
                <div class='kpi'><span>% Físico</span><b>{d['pct_phys']:.1f}%</b><small>Avanço de entregas</small></div>
                <div class='kpi'><span>% Financeiro</span><b>{pct_fin_str}</b><small>Orçamento (AC) consumido</small></div>
            </div>
            <div class='progress-grid'>
                <div class='progress-card'><span>Volume de Tarefas Concluídas</span><b>{d['pct_done']:.1f}%</b><div class='bar-bg'><div class='bar-fill' style='width:{d['pct_done']}%'></div></div></div>
                <div class='progress-card'><span>Avanço Físico Ponderado</span><b>{d['pct_phys']:.1f}%</b><div class='bar-bg'><div class='bar-fill' style='width:{d['pct_phys']}%'></div></div></div>
                <div class='progress-card'><span>Consumo Financeiro (Burn rate)</span><b>{pct_fin_str}</b><div class='bar-bg'><div class='bar-fill {fin_warn_bar}' style='width:{fin_bar_width}'></div></div></div>
            </div>
        </section>

        <!-- NOVO: TRACKER INSERIDO AQUI DENTRO DO LAYOUT PREMIUM -->
        <section class='section' id='timeline'><h2>Linha do Tempo (Marcos do Projeto)</h2>
            <div class="tracker-container">
                <ul class="tracker">
                    {tracker_html}
                </ul>
            </div>
        </section>
        
        <section class='section' id='gantt'><h2>Gantt Interativo (WBS)</h2>
            <div class='gantt-tools'>
                <div>
                    <button onclick='expandAll()'>Expandir Tudo</button>
                    <button onclick='collapseAll()'>Recolher Tudo</button>
                    <button onclick='showOnlyLate()'>Filtrar Atrasadas</button>
                    <button onclick='showAllRows()'>Limpar Filtros</button>
                </div>
                <input id='search' placeholder='Pesquisar tarefa, responsável, status...' oninput='filterRows()'>
            </div>
            <div class='gantt'>
                {gantt_html}
            </div>
        </section>
        
        <section class='section' id='atrasos'><h2>Detalhamento de Atrasos (Tarefas Folha)</h2>
            <div class='tw'><table><thead><tr><th>UID</th><th>Tarefa</th><th>Owner</th><th>Progresso</th><th>Baseline Fim</th><th>Data Atual Projetada</th><th>Variação</th></tr></thead>
            <tbody>{delays_html}</tbody></table></div>
        </section>
        
        <section class='section' id='eva'><h2>Análise de Valor Agregado (EVM)</h2>
            {eva_content}
        </section>
    </div>
    
    <!-- MODAL RESTAURADO -->
    <div class='modal-backdrop' id='modalBackdrop' onclick='closeModal(event)'><div class='modal' onclick='event.stopPropagation()'>
        <button class='close' onclick='hideModal()'>Fechar</button>
        <h2 id='modalTitle' style='font-size:24px; color:#0f172a; margin-bottom: 4px;'>Detalhe</h2><p id='modalSub' style='color:#64748b; margin-top:0;'></p>
        <div class='detail-grid' id='modalGrid'></div>
        <div id='modalChildren' style='margin-top:24px; padding-top: 24px; border-top: 1px solid #e2e8f0; color: #334155;'></div>
    </div></div>
    
    <script>
    const tasks = {tasks_json};
    const byUid = Object.fromEntries(tasks.map(t => [String(t.uid), t]));
    const expanded = new Set();
    
    function isAncestorExpanded(uid) {{
        let p = byUid[uid].parent;
        while (p && p !== "") {{
            if (!expanded.has(String(p))) return false;
            p = byUid[p].parent;
        }}
        return true;
    }}
    
    function toggleOrDetail(uid){{
        const t = byUid[String(uid)];
        if(t.children > 0) togglePhase(uid); else showDetail(uid);
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
            
            if (!parentId || parentId === "") {{
                row.classList.remove('hidden');
            }} else {{
                row.classList.toggle('hidden', !isAncestorExpanded(uid));
            }}
            
            if (byUid[uid].children > 0) {{
                const tgGantt = document.getElementById('tg-'+uid);
                const tgEva = document.getElementById('tg-eva-'+uid);
                const sign = expanded.has(uid) ? '−' : '+';
                if (tgGantt) tgGantt.textContent = sign;
                if (tgEva) tgEva.textContent = sign;
            }}
        }});
    }}
    
    function expandAll(){{ tasks.filter(t=>t.children > 0).forEach(t=>expanded.add(String(t.uid))); renderVisibility(); }}
    function collapseAll(){{ expanded.clear(); renderVisibility(); }}
    function showOnlyLate(){{ expandAll(); document.querySelectorAll('.gantt-row').forEach(row => row.classList.toggle('hidden', row.dataset.late !== '1')); }}
    function showAllRows(){{ document.getElementById('search').value=''; expandAll(); }}
    
    function filterRows(){{
        const q=document.getElementById('search').value.toLowerCase().trim();
        if(!q){{renderVisibility();return;}}
        expandAll();
        document.querySelectorAll('.gantt-row').forEach(row => {{
            const t = byUid[row.dataset.uid];
            row.classList.toggle('hidden', !(`${{t.name}} ${{t.status}}`.toLowerCase().includes(q)));
        }});
    }}
    
    function showDetail(uid){{
        const t=byUid[String(uid)]; 
        const children=tasks.filter(x=>x.parent===String(uid));
        
        document.getElementById('modalTitle').textContent=`${{t.name}}`;
        document.getElementById('modalSub').textContent=`Status: ${{t.status}}`;
        
        const grid=[['Início Baseline',t.b_start],['Fim Baseline',t.b_finish],['Início Atual',t.start],['Fim Atual',t.finish],['% Concluído',`${{t.pct}}%`],['Variação Prazo (SV)',`${{t.svd>0?'+':''}}${{t.svd}} dias`]];
        document.getElementById('modalGrid').innerHTML=grid.map(([k,v])=>`<div class='detail-box'><div class='detail-label'>${{k}}</div><div class='detail-value'>${{v}}</div></div>`).join('');
        
        document.getElementById('modalChildren').innerHTML=children.length?`<b style="font-size:16px">Subtarefas desta Fase</b><div style="margin-top:12px; display:grid; gap:8px;">${{children.map(c=>`<div style="background:#f8fafc; padding:10px 14px; border-radius:8px; font-size:13px; border:1px solid #e2e8f0; display:flex; justify-content:space-between"><span>${{c.name}}</span> <b>${{c.pct}}%</b></div>`).join('')}}</div>`:'<i>Esta é uma tarefa de trabalho folha (sem subtarefas associadas).</i>';
        
        document.getElementById('modalBackdrop').classList.add('flex');
    }}
    
    function hideModal(){{document.getElementById('modalBackdrop').classList.remove('flex');}}
    function closeModal(e){{if(e.target.id==='modalBackdrop')hideModal();}}
    
    collapseAll();
    </script></body></html>"""

    return html