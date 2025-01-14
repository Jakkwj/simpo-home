"use strict";(self.webpackChunksimpo_home=self.webpackChunksimpo_home||[]).push([[4817],{5991:(n,e,l)=>{l.r(e),l.d(e,{assets:()=>o,contentTitle:()=>d,default:()=>a,frontMatter:()=>r,metadata:()=>c,toc:()=>t});var i=l(4848),s=l(8453);const r={sidebar_position:11},d="2024",c={id:"SIMPO Pro/Earlier/2024",title:"2024",description:"2024-09-22",source:"@site/changelog/SIMPO Pro/Earlier/2024.md",sourceDirName:"SIMPO Pro/Earlier",slug:"/SIMPO Pro/Earlier/2024",permalink:"/zh/changelog/SIMPO Pro/Earlier/2024",draft:!1,unlisted:!1,tags:[],version:"current",sidebarPosition:11,frontMatter:{sidebar_position:11},sidebar:"docs",previous:{title:"2025",permalink:"/zh/changelog/SIMPO Pro/2025"},next:{title:"2023",permalink:"/zh/changelog/SIMPO Pro/Earlier/2023"}},o={},t=[{value:"2024-09-22",id:"2024-09-22",level:2},{value:"2024-08-09",id:"2024-08-09",level:2},{value:"2024-08-04",id:"2024-08-04",level:2},{value:"2024-05-11",id:"2024-05-11",level:2},{value:"2024-05-08",id:"2024-05-08",level:2},{value:"2024-05-07",id:"2024-05-07",level:2},{value:"2024-05-04",id:"2024-05-04",level:2},{value:"2024-05-03",id:"2024-05-03",level:2},{value:"2024-05-02",id:"2024-05-02",level:2},{value:"2024-04-28",id:"2024-04-28",level:2},{value:"2024-04-07",id:"2024-04-07",level:2}];function h(n){const e={code:"code",h1:"h1",h2:"h2",header:"header",li:"li",p:"p",ul:"ul",...(0,s.R)(),...n.components};return(0,i.jsxs)(i.Fragment,{children:[(0,i.jsx)(e.header,{children:(0,i.jsx)(e.h1,{id:"2024",children:"2024"})}),"\n",(0,i.jsx)(e.h2,{id:"2024-09-22",children:"2024-09-22"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Added"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Add Pareto figure in Sensitivity."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Improved"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"NEGATIVE ERROR and IMPROVED WARNING will send to dash frontend."}),"\n",(0,i.jsx)(e.li,{children:"Use -1 to reshape result."}),"\n",(0,i.jsx)(e.li,{children:"Async write report file."}),"\n",(0,i.jsx)(e.li,{children:"Async write biomatrix, kernel, input fortran files."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Fixed"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Fixed some known bugs."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-08-09",children:"2024-08-09"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Improved"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["Change ",(0,i.jsx)(e.code,{children:"Pandas"})," ",(0,i.jsx)(e.code,{children:"loc"}),"/",(0,i.jsx)(e.code,{children:"iloc"})," to ",(0,i.jsx)(e.code,{children:"at"}),"/",(0,i.jsx)(e.code,{children:"iat"}),"."]}),"\n",(0,i.jsx)(e.li,{children:"Change all fortran writter to f-string."}),"\n",(0,i.jsx)(e.li,{children:"Imporved matplotlib plotting."}),"\n",(0,i.jsx)(e.li,{children:"Change scatter plot to line plot, cause line plot is quicker."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-08-04",children:"2024-08-04"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Improved"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["Upgrade the ",(0,i.jsx)(e.code,{children:"Python"})," version to ",(0,i.jsx)(e.code,{children:"3.12"}),"."]}),"\n",(0,i.jsxs)(e.li,{children:["Change logger to ",(0,i.jsx)(e.code,{children:"Loguru"}),"."]}),"\n",(0,i.jsx)(e.li,{children:"Add more multiprocessing async pool in parsing input BioModel and DataSet, fortran file writting."}),"\n",(0,i.jsx)(e.li,{children:"Add color to SludgeError."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Changed"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"DataSet will be built partly in Solution.Build() to decouple with BioModel, in order to make use of multiprocessing async pool."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-05-11",children:"2024-05-11"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["Fixed","\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Remove counter_steady judger, only use counter_max_steady as the GA steady judger."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-05-08",children:"2024-05-08"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Added"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Add check.PoolExceptions to catch the pool.apply_async() exception."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Changed"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Changed all logger.debug() to logger.error()."}),"\n",(0,i.jsx)(e.li,{children:"plotter_pro.plot_Skeleton() will not plot webp format for now."}),"\n",(0,i.jsx)(e.li,{children:"Set pool in the right place in project.process_save_plot_evaluation()."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Fixed"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Fixed some known bugs."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-05-07",children:"2024-05-07"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Added"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Add '.done_plotting' marker file to indicate whether finish the plotting task."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Fixed"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Fixed some known bugs."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-05-04",children:"2024-05-04"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Added"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Add auto_plot_correlation to skip plot_OAT_Corr(), since this could take a very long time if data is large."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Improved"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Improved result+pro.get_result_OAT() to avoid PerformanceWarning: DataFrame is highly fragmented."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Fixed"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Fixed some known bugs."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-05-03",children:"2024-05-03"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["Improved","\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Remove empty check in Solution_pro._sync_group_component_evaluation()."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-05-02",children:"2024-05-02"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Added"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Add Build_frontend() to fit the frontend Create/Edit/Save Project check."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-04-28",children:"2024-04-28"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["Changed","\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Changed 'is True'/'is False' to '== True'/'== False' to avoid pd.DataFrame problem."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["Fixed","\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"Result.save_result_OAT()/save_result_KS() to_excel will have different sheetname."}),"\n"]}),"\n"]}),"\n"]}),"\n",(0,i.jsx)(e.h2,{id:"2024-04-07",children:"2024-04-07"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Changed"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"If TSS are all 0, the Estimation task won't start."}),"\n"]}),"\n"]}),"\n",(0,i.jsxs)(e.li,{children:["\n",(0,i.jsx)(e.p,{children:"Improved"}),"\n",(0,i.jsxs)(e.ul,{children:["\n",(0,i.jsx)(e.li,{children:"evaluation_abc.assign_xxx() functions will assing in the beginning of main_Evaluation.f90, then assign inside the parallel loop and then only assign again the change value."}),"\n"]}),"\n"]}),"\n"]})]})}function a(n={}){const{wrapper:e}={...(0,s.R)(),...n.components};return e?(0,i.jsx)(e,{...n,children:(0,i.jsx)(h,{...n})}):h(n)}},8453:(n,e,l)=>{l.d(e,{R:()=>d,x:()=>c});var i=l(6540);const s={},r=i.createContext(s);function d(n){const e=i.useContext(r);return i.useMemo((function(){return"function"==typeof n?n(e):{...e,...n}}),[e,n])}function c(n){let e;return e=n.disableParentContext?"function"==typeof n.components?n.components(s):n.components||s:d(n.components),i.createElement(r.Provider,{value:e},n.children)}}}]);