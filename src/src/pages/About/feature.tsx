import React from 'react';
import clsx from 'clsx';
// import Translate from '@docusaurus/Translate'
import styles from './index.module.css';
// import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl'
// import ThemedImage from '@theme/ThemedImage';

interface Props {
  imgUrl: string;
  title: JSX.Element | string;
  description: JSX.Element;
  reverse: boolean;
  width?: string;
  marginTop?: string;
}


// export default function Feature({ imgUrl, title, description, reverse, width='100%', marginTop='0vh' }: Props) {
export default function Feature({ imgUrl, title, description, width='100%', marginTop='0vh' }: Props) {
  return (
    // <div className={clsx('row', styles.feature, reverse && styles.featureReverse)}>
    <div className={clsx('row', styles.feature)}>
      <div className="col col--2 text--left" style={{marginLeft: '0vw', marginTop: '1vh'}}>
        {/* <img className={styles.featureImage} src={useBaseUrl(imgUrl)} alt={title}/> */}
        <img src={useBaseUrl(imgUrl)} alt={title as string} width={width}/>

      </div>
      <div className={clsx('col col--10 text--left', styles.featureContent)}>
        <div style={{marginTop: marginTop}}>
          <h3>{title}</h3>
          <div>{description}</div>
        </div>
      </div>
    </div>
  )
}
