"use strict";(self.webpackChunksimpo_home=self.webpackChunksimpo_home||[]).push([[4583],{4873:(e,i,n)=>{n.r(i),n.d(i,{default:()=>C});n(6540);var t=n(4586),r=n(3296),s=n(53),a=n(8774),o=n(1122),c=n(1312),l=n(4848);function d(){const{siteConfig:e}=(0,t.A)();return(0,l.jsxs)("header",{className:(0,s.A)("hero noise-bg"),children:[(0,l.jsx)("div",{className:"col col--1 text-center",style:{marginRight:"1.2vw"}}),(0,l.jsxs)("div",{className:"col col--6 text-center",children:[(0,l.jsxs)("div",{className:"container",children:[(0,l.jsx)("div",{className:"row",style:{marginTop:"-1.5vh",color:"#eee"},children:(0,l.jsx)("h1",{style:{marginBottom:"0vh",color:"#eee"},className:"hero__title",children:e.title})}),(0,l.jsx)("div",{className:"row",style:{marginTop:"0vh",color:"#eee"},children:(0,l.jsx)("p",{style:{marginRight:"10vw",marginBottom:"0.8vh",color:"#eee"},className:"hero__subtitle",children:(0,l.jsx)(c.A,{id:"tagline",children:"A Scientific Computing SaaS Platform for Water and Wastewater Treatment Process Modeling"})})}),(0,l.jsx)("div",{className:"row",style:{marginTop:"0vh",color:"#eee"},children:(0,l.jsxs)("p",{style:{color:"#eee"},className:"",children:[e.title," ",(0,l.jsx)(c.A,{children:"combines user-friendliness with power and flexibility, it is an open-minded modern cloud-based platform for water and wastewater treatment process modeling."})," ",e.title," ",(0,l.jsx)(c.A,{children:"aims to lower the learning and research barriers for modelling, improve development efficiency, provide scientific algorithms and evaluation methods, and ultimately achieve a sustainable intelligent big data platform for co-creation, sharing and providing Open Educational Resources (OER) for all."})]})})]}),(0,l.jsxs)("div",{className:"",style:{marginTop:"1vh"},children:[(0,l.jsx)(a.A,{href:"docs",className:"button button--secondary",children:(0,l.jsx)(c.A,{children:"Quick Start"})}),(0,l.jsx)(a.A,{children:" \xa0 "}),(0,l.jsxs)("div",{className:"button button--secondary dropdown",children:[(0,l.jsx)(c.A,{children:"Client"})," \xa0 >",(0,l.jsxs)("div",{className:"dropdown-content",children:[(0,l.jsx)("a",{href:e.customFields.urlDownloadClientWindows,download:!0,children:"Windows"}),(0,l.jsx)("a",{href:e.customFields.urlDownloalNetdisk,target:"_blank",rel:"noopener noreferrer",children:"Windows (Netdisk)"}),(0,l.jsx)("a",{href:e.customFields.urlDownloalClientUbuntu,download:!0,children:"Ubuntu"}),(0,l.jsx)("a",{href:"#",style:{cursor:"default",color:"gray"},children:"Mac (pending...)"})]})]})]})]}),(0,l.jsx)("div",{className:"col hero-image",style:{marginRight:"0vw"},children:(0,l.jsx)(o.A,{sources:{light:e.customFields.imgUrlBanner,dark:e.customFields.imgUrlBanner},alt:"Preview of using SIMPO",width:"75%"})})]})}var h=n(8453),m=n(1873);function u(e){return(0,l.jsx)(m.K,{chart:"gantt\n  dateFormat  YYYY-MM-DD\n  axisFormat  %Y-%m\n  tickInterval 6month\n  todayMarker on\n  title       Developed Timeline\n  excludes    weekends\n  section SIMPO\n  Standardized Input Template             :done, a1a, 2018-01-01, 2019-10-01\n  Simulation Engine                       :crit, done, a1b, 2018-02-01, 2020-10-01\n  Connected to Simpo Dash                 :done, a2, after a1b, 2022-10-01\n  Version Control                         :done, a12, 2022-08-01, 2023-05-01\n  section SIMPO Pro\n  Sensitivity Engine                      :crit, done, b1a, 2018-01-01, 2019-01-01\n  Uncertainty Engine                      :crit, done, b1b, after b1a, 2020-01-01\n  Estimation Engine                       :crit, done, b1c, after b1b, 2021-01-01\n  Connected to Simpo Dash                 :done, b2, after b1c, 2022-12-01\n\n  pH Calculation                          :crit, active, b3, after c4apH, 30d\n  SEC-UA                                  :crit, b4, after c4a02, 30d\n  Automatic Evaluation                    :crit, c4a03, after c4a02, 90d\n  10 Layer Settling Reactor               :crit, c4a04, after c4a03, 60d\n  Standardized Repositories               :c5Repositories, after c4a04, 30d\n  Standardized Rate                       :crit, c5Rate, after c5Repositories, 30d\n  Automatic Construct BioModel            :crit, c5, after c5Rate, 30d\n\n  GPU capacity                            :c9, after c5, 300d\n  AI Algorithm                            :crit, c6, after c9, 300d\n  Mechanism + Blackbox Model              :crit, milestone, mc3, after c6, 0d\n  PlugFlow Reactor                        :c4c, after c6, 60d\n  BioFilm Reactor                         :c4d, after c4c, 90d\n  Sewer Reactor                           :c4e, after c4d, 90d\n  Real-Time Support                       :c5a, after c4e, 300d\n  Steady State                            :c4StedayState, after c4e, 120d\n  CFD Algorithm                           :c7, after c4StedayState, 300d\n\n  section SIMPO Dash\n  Web Frontend/Backend Core Function      :crit, done, c1, 2018-10-01, 2023-01-01\n  Basic Function Stable                   :crit, milestone, mc1, after c1, 0d\n  FlowChart                               :crit, done, c12, after c1, 90d\n  Http to Https                           :done, c2, 2023-05-01, 2023-06-10\n  Estimaiton Engine                       :crit, done, c3, after c2, 2023-12-31\n  Uncertainty Engine                      :crit, done, c4, after c2, 2023-12-31\n  FlowChart Upgrade                       :done, c40, after c4, 2024-04-23\n  AI (Kimi) Support                       :done, c40kimi, after c40, 2024-06-23\n  BioModel Composition                    :done, c4aComposition, after c40kimi, 2024-12-18\n\n  Estimaiton Plotting                     :crit, c4a01, after b3, 60d\n  Uncertainty Plotting                    :crit, c4a02, after b3, 60d\n  Enhanced Function Stable                :crit, milestone, mc2, after c4a02, 0d\n\n\n  3D Digital Twin                         :c8, after c7, 300d\n  Discussion Board                        :c10, after c7, 300d\n"})}function g(e={}){const{wrapper:i}={...(0,h.R)(),...e.components};return i?(0,l.jsx)(i,{...e,children:(0,l.jsx)(u,{...e})}):u()}function p(){const{siteConfig:e}=(0,t.A)();return(0,l.jsx)("div",{className:"hero",style:{marginTop:"-9vh"},children:(0,l.jsxs)("div",{className:"container text-center",children:[(0,l.jsx)("hr",{style:{marginTop:"2.8vh",marginBottom:"3vh",paddingLeft:"18vw",paddingRight:"18vw"}}),(0,l.jsx)("h1",{className:"text-center",children:"Roadmap"}),"This is the raodmap of ",(0,l.jsx)("b",{children:"SIMPO"}),". For more details please refer to: ",(0,l.jsx)("a",{href:"changelog",children:"Changelog"}),".",(0,l.jsx)(g,{name:"Gantt"})]})})}const x={heroLogoWrapper:"heroLogoWrapper_xRBc",heroLogo:"heroLogo_a2VX",heroTitle:"heroTitle_XKgo",feature:"feature_pWM7",featureReverse:"featureReverse_A6CJ",featureImage:"featureImage_IMyC",featureContent:"featureContent_CRI5",whiteboard:"whiteboard_ASIa",whiteboardCol:"whiteboardCol_pyfT",logoWrapper:"logoWrapper_PvjK",cncfLogo:"cncfLogo_G5Ll"};var f=n(6025);function j(e){let{imgUrl:i,title:n,description:t,reverse:r,width:a="100%",marginTop:o="0vh"}=e;return(0,l.jsxs)("div",{className:(0,s.A)("row",x.feature,r&&x.featureReverse),children:[(0,l.jsx)("div",{className:"col col--6 text--center",children:(0,l.jsx)("img",{src:(0,f.Ay)(i),alt:n,width:a})}),(0,l.jsx)("div",{className:(0,s.A)("col col--6",x.featureContent),children:(0,l.jsxs)("div",{style:{marginTop:o},children:[(0,l.jsx)("h3",{children:n}),(0,l.jsx)("div",{children:t})]})})]})}function v(){const{siteConfig:e}=(0,t.A)();return(0,l.jsx)("div",{className:"hero",style:{marginTop:"0vh"},children:(0,l.jsx)("div",{className:"container",children:(0,l.jsx)(j,{reverse:!1,width:"90%",imgUrl:e.customFields.imgUrlTheEasiestWay,title:(0,l.jsx)(c.A,{id:"home.easytouse",children:"Easy to Use"}),description:(0,l.jsxs)(l.Fragment,{children:[(0,l.jsx)("p",{children:(0,l.jsx)(c.A,{id:"home.easytouse.1",children:"Let you focus on your model deducing and experimental datas, we'll do the computing:"})}),(0,l.jsxs)("ul",{children:[(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{id:"home.easytouse.2",children:"Through the user-friendly front-end interface, model building can be done quickly without any programming."})}),(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{id:"home.easytouse.3",children:"The input of models and data can be accomplished through: 1) importing xlsx files, 2) copying public models/data, or 3) creating new ones directly."})}),(0,l.jsxs)("li",{children:[e.title,(0,l.jsx)(c.A,{id:"home.easytouse.4",children:" will automatically generate a process flow diagram and a series of graphs of the calculation results, users can export the result data for further processing."})]})]})]})})})})}function y(){const{siteConfig:e}=(0,t.A)();return(0,l.jsx)("div",{className:"hero",style:{marginTop:"-10vh"},children:(0,l.jsx)("div",{className:"container",children:(0,l.jsx)(j,{reverse:!0,width:"80%",marginTop:"2.6vh",imgUrl:e.customFields.imgUrlPowerful,title:(0,l.jsx)(c.A,{id:"home.powerful",children:"Powerful and Flexible"}),description:(0,l.jsxs)(l.Fragment,{children:[(0,l.jsx)("p",{children:(0,l.jsx)(c.A,{children:"Provides various calculation engines and functions:"})}),(0,l.jsxs)("ul",{children:[(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{children:"Calculation engines includes: simulation, sensitivity analysis, uncertainty analysis and parameter estimation."})}),(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{children:"Models and data can be combined in any way users see fit, so it's very easy to identify the optimal model for a given dataset and evaluate a model's robustness and generalizability."})}),(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{children:"Models and data can be released in multiple versions, making it easy to determine the optimal model structure and parameter."})})]})]})})})})}function b(){const{siteConfig:e}=(0,t.A)();return(0,l.jsx)("div",{className:"hero",style:{marginTop:"-6vh"},children:(0,l.jsx)("div",{className:"container",children:(0,l.jsx)(j,{reverse:!1,width:"90%",imgUrl:e.customFields.imgUrlOpen,title:(0,l.jsx)(c.A,{id:"home.open",children:"Open-Minded"}),description:(0,l.jsxs)(l.Fragment,{children:[(0,l.jsx)("p",{children:(0,l.jsx)(c.A,{children:"An open-minded platform that provides OER for everyone:"})}),(0,l.jsxs)("ul",{children:[(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{children:"Everyone is encouraged to contribute code to co-create algorithms."})}),(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{children:"Works on Windows, Linux, and Mac, it can leverage the power of supercomputers, as their systems are usually Linux-based."})}),(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{children:"Models, datasets and calculation results can be published in public version to share the research findings to the entire research community."})}),(0,l.jsxs)("li",{children:[e.title,(0,l.jsx)(c.A,{id:"home.open.3",children:" provides OER to all researchers and students. This endeavor aligns with the United Nations' Sustainable Development Goal 4: Quality Education."})]})]})]})})})})}function w(){const{siteConfig:e}=(0,t.A)();return(0,l.jsx)("div",{className:"hero",style:{marginTop:"-10vh"},children:(0,l.jsx)("div",{className:"container",children:(0,l.jsx)(j,{reverse:!0,marginTop:"2.6vh",imgUrl:e.customFields.imgUrlTrackable,title:(0,l.jsx)(c.A,{id:"home.trackable",children:"Trackable"}),description:(0,l.jsxs)(l.Fragment,{children:[(0,l.jsx)("p",{children:(0,l.jsx)(c.A,{children:"No way to cheat:"})}),(0,l.jsxs)("ul",{children:[(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{children:"All results are calculated according to open-source code, there is no possibility of modifying the calculation results."})}),(0,l.jsx)("li",{children:(0,l.jsx)(c.A,{children:"All model submissions can be calculated and published publicly, thereby precluding the possibility of algorithmic cheating."})})]})]})})})})}function A(){const{siteConfig:e}=(0,t.A)();return(0,l.jsx)("div",{className:"hero",style:{marginTop:"-6vh"},children:(0,l.jsx)("div",{className:"container",children:(0,l.jsx)(j,{reverse:!1,width:"90%",imgUrl:e.customFields.imgUrlResource,title:(0,l.jsx)(c.A,{id:"home.collaboration",children:"Collaboration is welcome"}),description:(0,l.jsx)(l.Fragment,{children:(0,l.jsxs)("ul",{children:[(0,l.jsxs)("li",{children:[(0,l.jsx)(c.A,{children:"Join us in building and enhancing "}),(0,l.jsx)("a",{href:"https://www.simpowater.org/resource",children:"Paper Resource"}),(0,l.jsx)(c.A,{children:" with the help of powerful AI tools. Your contributions can significantly enhance and expand the collection, making it more valuable for the entire community.\n                  "})]}),(0,l.jsxs)("li",{children:[(0,l.jsx)(c.A,{children:"We appreciate your support and collaboration, fork and pull request are welcome in: "}),(0,l.jsx)("a",{href:"https://github.com/Jakkwj/simpo-home",children:"simpo-home"})]})]})})})})})}function C(){const{siteConfig:e}=(0,t.A)();return(0,l.jsxs)(r.A,{title:"Home",description:"Description will go into a meta tag in <head />",children:[(0,l.jsx)(d,{}),(0,l.jsxs)("main",{children:[(0,l.jsx)(v,{}),(0,l.jsx)(y,{}),(0,l.jsx)(b,{}),(0,l.jsx)(w,{}),(0,l.jsx)(A,{}),(0,l.jsx)(p,{})]})]})}}}]);