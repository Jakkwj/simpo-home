import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import assessmentCases from './dynamicAssessment';

// MATLAB R2024b trajectories and perf_plant.m output; SIMPO case 04 at 0.01% Step Tolerance.
type Reading = [en: string, zh: string, unit: string, matlab: number, simpo: number, decimals: number];
const metricLabels: Record<string, [string, string, string, number]> = {
  EQ: ['Effluent quality', '出水污染负荷', 'kg pollution units/d', 4],
  SP: ['Sludge production', '污泥产量', 'kg SS/d', 4],
  AE: ['Aeration energy', '曝气耗电', 'kWh/d', 4],
  PE: ['Pumping energy', '泵送耗电', 'kWh/d', 4],
  EC: ['External carbon', '外加碳源', 'kg COD/d', 0],
  ME: ['Mixing energy', '搅拌耗电', 'kWh/d', 0],
  OCI: ['Operating cost index', '运行成本指数', '–', 4],
};
const assessment = assessmentCases.find(row => row.id === '04')!;
const groups: {name: string; readings: Reading[]}[] = [
  {name: 'Tank2 → Q_a', readings: [
    ['Mean absolute process error', '工艺值平均绝对偏差', 'g N/m³', 0.2057337448312434, 0.2057333741871544, 8],
    ['Total handle movement', '操纵量累计变化量', 'm³/d', 4065304.5253461422, 4064634.541030781, 2],
    ['Time at limit', '触限时间占比', '%', 6.063988095238095, 6.063988095238095, 6],
  ]},
  {name: 'Tank5 → KLa_5', readings: [
    ['Mean absolute process error', '工艺值平均绝对偏差', 'g O₂/m³', 0.0878882113200999, 0.0879082578032211, 8],
    ['Total handle movement', '操纵量累计变化量', 'd⁻¹', 13306.654772621232, 13309.537293595164, 3],
    ['Time at limit', '触限时间占比', '%', 0.0372023809523809, 0.0372023809523809, 6],
  ]},
  {name: 'Assessment', readings: assessment.readings.map(({metric, matlab, tight}): Reading => {
    const [en, zh, unit, decimals] = metricLabels[metric];
    return [metric + ' · ' + en, metric + ' · ' + zh, unit, matlab, tight, decimals];
  })},
];

function relativeDifference(matlab: number, simpo: number): string {
  if (matlab === 0) return '—';
  const difference = 100 * (simpo - matlab) / matlab;
  if (difference === 0) return '0%';
  if (Math.abs(difference) < 0.0000005) return '≈ 0%';
  return (difference > 0 ? '+' : '−') + Math.abs(difference).toFixed(6) + '%';
}

export default function Case04Comparison({controllersOnly = false}: {controllersOnly?: boolean}) {
  const zh = useDocusaurusContext().i18n.currentLocale === 'zh';
  const text = (en: string, cn: string) => zh ? cn : en;
  const number = (value: number, decimals: number) => value.toLocaleString(zh ? 'zh-CN' : 'en-US', {
    minimumFractionDigits: decimals, maximumFractionDigits: decimals,
  });
  const visibleGroups = controllersOnly ? groups.filter(group => group.name !== 'Assessment') : groups;
  return <table aria-label={controllersOnly
    ? text('Case 04 controller comparison', '案例 04 控制器对照')
    : text('Case 04 dry closed-loop comparison', '案例 04 晴天闭环对照')}>
    <thead><tr>
      <th scope="col">{text('Loop / plant', '回路 / 全厂')}</th>
      <th scope="col">{text('Metric', '指标')}</th><th scope="col">{text('Unit', '单位')}</th>
      <th scope="col">MATLAB R2024b</th><th scope="col">SIMPO (0.01%)</th>
      <th scope="col">{text('Relative difference', '相对差')}</th>
    </tr></thead>
    {visibleGroups.map(group => <tbody key={group.name}>
      {group.readings.map(([en, cn, unit, matlab, simpo, decimals], index) => <tr key={en}>
        {index === 0 && <th scope="rowgroup" rowSpan={group.readings.length}>{group.name}</th>}
        <th scope="row">{text(en, cn)}</th>
        <td>{unit === 'kg pollution units/d' ? text('kg pollution units/d', 'kg 污染当量/d') : unit}</td>
        <td align="right">{number(matlab, decimals)}</td><td align="right">{number(simpo, decimals)}</td>
        <td align="right">{relativeDifference(matlab, simpo)}</td>
      </tr>)}
    </tbody>)}
  </table>;
}
