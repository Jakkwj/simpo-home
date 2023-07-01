
import React from 'react';
import Translate from '@docusaurus/Translate'
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
// import PartialExample from './_markdown-partial-example.mdx';
import TimeLine from './timeline.mdx';
import Gantt from './gantt.mdx';


export default function FeaturesOpen() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <div className="hero" style={{marginTop: '-6vh'}}>
      <div className="container text-center" >
        <h1 className="text-center">Roadmap</h1>
        This is the raodmap of <b>SIMPO</b>. For more details please refer to: <a href="docs/category/changelog">Changelog</a>.

       {/* <TimeLine name="TimeLine" /> */}

       <Gantt name="Gantt" />

      </div>
    </div>
  );
}
