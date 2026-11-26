import React from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import cases from './dynamicAssessment';
import styles from './DynamicAssessmentComparison.module.css';

export default function DynamicAssessmentComparison() {
  const zh = useDocusaurusContext().i18n.currentLocale === 'zh';
  return <table className={styles.comparison} aria-label={zh ? '六个动态案例的 Assessment 对照' : 'Assessment comparison for the six dynamic cases'}>
    <thead><tr>
      <th scope="col">{zh ? '工况' : 'Case'}</th>
      <th scope="col">{zh ? '指标' : 'Metric'}</th>
      <th scope="col">{zh ? '2008 年' : '2008'} <span style={{whiteSpace: 'nowrap'}}>{zh ? '原报告' : 'report'}</span></th>
      <th scope="col">MATLAB R2024b</th>
      <th scope="col">SIMPO (0.01%)</th>
      <th scope="col">SIMPO (5%)</th>
      <th scope="col">{zh ? '差值与原因' : 'Difference and explanation'}</th>
    </tr></thead>
    {cases.map(({id, en, zh: chineseName, readings}) => <tbody key={id}>
      {readings.map((row, index) => {
        const decimals = row.metric === 'EC' || row.metric === 'ME' ? 0 : 4;
        const difference = row.tight - row.matlab;
        const magnitude = Math.abs(difference).toFixed(decimals);
        const showExplanation = Number(magnitude) !== 0;
        const sign = showExplanation ? (difference > 0 ? '+' : '−') : '';
        return <tr key={row.metric}>
          {index === 0 && <th scope="rowgroup" rowSpan={readings.length} style={{verticalAlign: 'top'}}>
            {id} <span style={{whiteSpace: 'nowrap'}}>{zh ? chineseName : en}</span>
          </th>}
          <th scope="row">{row.metric}</th>
          {[row.report, row.matlab, row.tight, row.saved].map((value, column) =>
            <td align="right" key={column}>{value.toFixed(decimals)}</td>)}
          <td className={styles.analysis}>
            <strong>{sign}{magnitude}</strong>
            {showExplanation && <> {zh ? row.zh : row.en}</>}
          </td>
        </tr>;
      })}
    </tbody>)}
  </table>;
}
