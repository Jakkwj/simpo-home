"use strict";(self.webpackChunksimpo_home=self.webpackChunksimpo_home||[]).push([[5422],{5422:(t,e,n)=>{n.d(e,{diagram:()=>D});var i=n(9331),s=n(6312),r=n(2516),a=(n(4353),n(6750),n(2838),function(){var t=function(t,e,n,i){for(n=n||{},i=t.length;i--;n[t[i]]=e);return n},e=[1,2],n=[1,5],i=[6,9,11,17,18,20,22,23,24,26],s=[1,15],r=[1,16],a=[1,17],o=[1,18],c=[1,19],l=[1,20],h=[1,24],u=[4,6,9,11,17,18,20,22,23,24,26],y={trace:function(){},yy:{},symbols_:{error:2,start:3,journey:4,document:5,EOF:6,directive:7,line:8,SPACE:9,statement:10,NEWLINE:11,openDirective:12,typeDirective:13,closeDirective:14,":":15,argDirective:16,title:17,acc_title:18,acc_title_value:19,acc_descr:20,acc_descr_value:21,acc_descr_multiline_value:22,section:23,taskName:24,taskData:25,open_directive:26,type_directive:27,arg_directive:28,close_directive:29,$accept:0,$end:1},terminals_:{2:"error",4:"journey",6:"EOF",9:"SPACE",11:"NEWLINE",15:":",17:"title",18:"acc_title",19:"acc_title_value",20:"acc_descr",21:"acc_descr_value",22:"acc_descr_multiline_value",23:"section",24:"taskName",25:"taskData",26:"open_directive",27:"type_directive",28:"arg_directive",29:"close_directive"},productions_:[0,[3,3],[3,2],[5,0],[5,2],[8,2],[8,1],[8,1],[8,1],[7,4],[7,6],[10,1],[10,2],[10,2],[10,1],[10,1],[10,2],[10,1],[12,1],[13,1],[16,1],[14,1]],performAction:function(t,e,n,i,s,r,a){var o=r.length-1;switch(s){case 1:return r[o-1];case 3:case 7:case 8:this.$=[];break;case 4:r[o-1].push(r[o]),this.$=r[o-1];break;case 5:case 6:this.$=r[o];break;case 11:i.setDiagramTitle(r[o].substr(6)),this.$=r[o].substr(6);break;case 12:this.$=r[o].trim(),i.setAccTitle(this.$);break;case 13:case 14:this.$=r[o].trim(),i.setAccDescription(this.$);break;case 15:i.addSection(r[o].substr(8)),this.$=r[o].substr(8);break;case 16:i.addTask(r[o-1],r[o]),this.$="task";break;case 18:i.parseDirective("%%{","open_directive");break;case 19:i.parseDirective(r[o],"type_directive");break;case 20:r[o]=r[o].trim().replace(/'/g,'"'),i.parseDirective(r[o],"arg_directive");break;case 21:i.parseDirective("}%%","close_directive","journey")}},table:[{3:1,4:e,7:3,12:4,26:n},{1:[3]},t(i,[2,3],{5:6}),{3:7,4:e,7:3,12:4,26:n},{13:8,27:[1,9]},{27:[2,18]},{6:[1,10],7:21,8:11,9:[1,12],10:13,11:[1,14],12:4,17:s,18:r,20:a,22:o,23:c,24:l,26:n},{1:[2,2]},{14:22,15:[1,23],29:h},t([15,29],[2,19]),t(i,[2,8],{1:[2,1]}),t(i,[2,4]),{7:21,10:25,12:4,17:s,18:r,20:a,22:o,23:c,24:l,26:n},t(i,[2,6]),t(i,[2,7]),t(i,[2,11]),{19:[1,26]},{21:[1,27]},t(i,[2,14]),t(i,[2,15]),{25:[1,28]},t(i,[2,17]),{11:[1,29]},{16:30,28:[1,31]},{11:[2,21]},t(i,[2,5]),t(i,[2,12]),t(i,[2,13]),t(i,[2,16]),t(u,[2,9]),{14:32,29:h},{29:[2,20]},{11:[1,33]},t(u,[2,10])],defaultActions:{5:[2,18],7:[2,2],24:[2,21],31:[2,20]},parseError:function(t,e){if(!e.recoverable){var n=new Error(t);throw n.hash=e,n}this.trace(t)},parse:function(t){var e=this,n=[0],i=[],s=[null],r=[],a=this.table,o="",c=0,l=0,h=r.slice.call(arguments,1),u=Object.create(this.lexer),y={yy:{}};for(var p in this.yy)Object.prototype.hasOwnProperty.call(this.yy,p)&&(y.yy[p]=this.yy[p]);u.setInput(t,y.yy),y.yy.lexer=u,y.yy.parser=this,void 0===u.yylloc&&(u.yylloc={});var d=u.yylloc;r.push(d);var f=u.options&&u.options.ranges;"function"==typeof y.yy.parseError?this.parseError=y.yy.parseError:this.parseError=Object.getPrototypeOf(this).parseError;for(var g,x,m,k,_,v,b,$,w,M={};;){if(x=n[n.length-1],this.defaultActions[x]?m=this.defaultActions[x]:(null==g&&(w=void 0,"number"!=typeof(w=i.pop()||u.lex()||1)&&(w instanceof Array&&(w=(i=w).pop()),w=e.symbols_[w]||w),g=w),m=a[x]&&a[x][g]),void 0===m||!m.length||!m[0]){var E="";for(_ in $=[],a[x])this.terminals_[_]&&_>2&&$.push("'"+this.terminals_[_]+"'");E=u.showPosition?"Parse error on line "+(c+1)+":\n"+u.showPosition()+"\nExpecting "+$.join(", ")+", got '"+(this.terminals_[g]||g)+"'":"Parse error on line "+(c+1)+": Unexpected "+(1==g?"end of input":"'"+(this.terminals_[g]||g)+"'"),this.parseError(E,{text:u.match,token:this.terminals_[g]||g,line:u.yylineno,loc:d,expected:$})}if(m[0]instanceof Array&&m.length>1)throw new Error("Parse Error: multiple actions possible at state: "+x+", token: "+g);switch(m[0]){case 1:n.push(g),s.push(u.yytext),r.push(u.yylloc),n.push(m[1]),g=null,l=u.yyleng,o=u.yytext,c=u.yylineno,d=u.yylloc;break;case 2:if(v=this.productions_[m[1]][1],M.$=s[s.length-v],M._$={first_line:r[r.length-(v||1)].first_line,last_line:r[r.length-1].last_line,first_column:r[r.length-(v||1)].first_column,last_column:r[r.length-1].last_column},f&&(M._$.range=[r[r.length-(v||1)].range[0],r[r.length-1].range[1]]),void 0!==(k=this.performAction.apply(M,[o,l,c,y.yy,m[1],s,r].concat(h))))return k;v&&(n=n.slice(0,-1*v*2),s=s.slice(0,-1*v),r=r.slice(0,-1*v)),n.push(this.productions_[m[1]][0]),s.push(M.$),r.push(M._$),b=a[n[n.length-2]][n[n.length-1]],n.push(b);break;case 3:return!0}}return!0}},p={EOF:1,parseError:function(t,e){if(!this.yy.parser)throw new Error(t);this.yy.parser.parseError(t,e)},setInput:function(t,e){return this.yy=e||this.yy||{},this._input=t,this._more=this._backtrack=this.done=!1,this.yylineno=this.yyleng=0,this.yytext=this.matched=this.match="",this.conditionStack=["INITIAL"],this.yylloc={first_line:1,first_column:0,last_line:1,last_column:0},this.options.ranges&&(this.yylloc.range=[0,0]),this.offset=0,this},input:function(){var t=this._input[0];return this.yytext+=t,this.yyleng++,this.offset++,this.match+=t,this.matched+=t,t.match(/(?:\r\n?|\n).*/g)?(this.yylineno++,this.yylloc.last_line++):this.yylloc.last_column++,this.options.ranges&&this.yylloc.range[1]++,this._input=this._input.slice(1),t},unput:function(t){var e=t.length,n=t.split(/(?:\r\n?|\n)/g);this._input=t+this._input,this.yytext=this.yytext.substr(0,this.yytext.length-e),this.offset-=e;var i=this.match.split(/(?:\r\n?|\n)/g);this.match=this.match.substr(0,this.match.length-1),this.matched=this.matched.substr(0,this.matched.length-1),n.length-1&&(this.yylineno-=n.length-1);var s=this.yylloc.range;return this.yylloc={first_line:this.yylloc.first_line,last_line:this.yylineno+1,first_column:this.yylloc.first_column,last_column:n?(n.length===i.length?this.yylloc.first_column:0)+i[i.length-n.length].length-n[0].length:this.yylloc.first_column-e},this.options.ranges&&(this.yylloc.range=[s[0],s[0]+this.yyleng-e]),this.yyleng=this.yytext.length,this},more:function(){return this._more=!0,this},reject:function(){return this.options.backtrack_lexer?(this._backtrack=!0,this):this.parseError("Lexical error on line "+(this.yylineno+1)+". You can only invoke reject() in the lexer when the lexer is of the backtracking persuasion (options.backtrack_lexer = true).\n"+this.showPosition(),{text:"",token:null,line:this.yylineno})},less:function(t){this.unput(this.match.slice(t))},pastInput:function(){var t=this.matched.substr(0,this.matched.length-this.match.length);return(t.length>20?"...":"")+t.substr(-20).replace(/\n/g,"")},upcomingInput:function(){var t=this.match;return t.length<20&&(t+=this._input.substr(0,20-t.length)),(t.substr(0,20)+(t.length>20?"...":"")).replace(/\n/g,"")},showPosition:function(){var t=this.pastInput(),e=new Array(t.length+1).join("-");return t+this.upcomingInput()+"\n"+e+"^"},test_match:function(t,e){var n,i,s;if(this.options.backtrack_lexer&&(s={yylineno:this.yylineno,yylloc:{first_line:this.yylloc.first_line,last_line:this.last_line,first_column:this.yylloc.first_column,last_column:this.yylloc.last_column},yytext:this.yytext,match:this.match,matches:this.matches,matched:this.matched,yyleng:this.yyleng,offset:this.offset,_more:this._more,_input:this._input,yy:this.yy,conditionStack:this.conditionStack.slice(0),done:this.done},this.options.ranges&&(s.yylloc.range=this.yylloc.range.slice(0))),(i=t[0].match(/(?:\r\n?|\n).*/g))&&(this.yylineno+=i.length),this.yylloc={first_line:this.yylloc.last_line,last_line:this.yylineno+1,first_column:this.yylloc.last_column,last_column:i?i[i.length-1].length-i[i.length-1].match(/\r?\n?/)[0].length:this.yylloc.last_column+t[0].length},this.yytext+=t[0],this.match+=t[0],this.matches=t,this.yyleng=this.yytext.length,this.options.ranges&&(this.yylloc.range=[this.offset,this.offset+=this.yyleng]),this._more=!1,this._backtrack=!1,this._input=this._input.slice(t[0].length),this.matched+=t[0],n=this.performAction.call(this,this.yy,this,e,this.conditionStack[this.conditionStack.length-1]),this.done&&this._input&&(this.done=!1),n)return n;if(this._backtrack){for(var r in s)this[r]=s[r];return!1}return!1},next:function(){if(this.done)return this.EOF;var t,e,n,i;this._input||(this.done=!0),this._more||(this.yytext="",this.match="");for(var s=this._currentRules(),r=0;r<s.length;r++)if((n=this._input.match(this.rules[s[r]]))&&(!e||n[0].length>e[0].length)){if(e=n,i=r,this.options.backtrack_lexer){if(!1!==(t=this.test_match(n,s[r])))return t;if(this._backtrack){e=!1;continue}return!1}if(!this.options.flex)break}return e?!1!==(t=this.test_match(e,s[i]))&&t:""===this._input?this.EOF:this.parseError("Lexical error on line "+(this.yylineno+1)+". Unrecognized text.\n"+this.showPosition(),{text:"",token:null,line:this.yylineno})},lex:function(){var t=this.next();return t||this.lex()},begin:function(t){this.conditionStack.push(t)},popState:function(){return this.conditionStack.length-1>0?this.conditionStack.pop():this.conditionStack[0]},_currentRules:function(){return this.conditionStack.length&&this.conditionStack[this.conditionStack.length-1]?this.conditions[this.conditionStack[this.conditionStack.length-1]].rules:this.conditions.INITIAL.rules},topState:function(t){return(t=this.conditionStack.length-1-Math.abs(t||0))>=0?this.conditionStack[t]:"INITIAL"},pushState:function(t){this.begin(t)},stateStackSize:function(){return this.conditionStack.length},options:{"case-insensitive":!0},performAction:function(t,e,n,i){switch(n){case 0:return this.begin("open_directive"),26;case 1:return this.begin("type_directive"),27;case 2:return this.popState(),this.begin("arg_directive"),15;case 3:return this.popState(),this.popState(),29;case 4:return 28;case 5:case 6:case 8:case 9:break;case 7:return 11;case 10:return 4;case 11:return 17;case 12:return this.begin("acc_title"),18;case 13:return this.popState(),"acc_title_value";case 14:return this.begin("acc_descr"),20;case 15:return this.popState(),"acc_descr_value";case 16:this.begin("acc_descr_multiline");break;case 17:this.popState();break;case 18:return"acc_descr_multiline_value";case 19:return 23;case 20:return 24;case 21:return 25;case 22:return 15;case 23:return 6;case 24:return"INVALID"}},rules:[/^(?:%%\{)/i,/^(?:((?:(?!\}%%)[^:.])*))/i,/^(?::)/i,/^(?:\}%%)/i,/^(?:((?:(?!\}%%).|\n)*))/i,/^(?:%(?!\{)[^\n]*)/i,/^(?:[^\}]%%[^\n]*)/i,/^(?:[\n]+)/i,/^(?:\s+)/i,/^(?:#[^\n]*)/i,/^(?:journey\b)/i,/^(?:title\s[^#\n;]+)/i,/^(?:accTitle\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*:\s*)/i,/^(?:(?!\n||)*[^\n]*)/i,/^(?:accDescr\s*\{\s*)/i,/^(?:[\}])/i,/^(?:[^\}]*)/i,/^(?:section\s[^#:\n;]+)/i,/^(?:[^#:\n;]+)/i,/^(?::[^#\n;]+)/i,/^(?::)/i,/^(?:$)/i,/^(?:.)/i],conditions:{open_directive:{rules:[1],inclusive:!1},type_directive:{rules:[2,3],inclusive:!1},arg_directive:{rules:[3,4],inclusive:!1},acc_descr_multiline:{rules:[17,18],inclusive:!1},acc_descr:{rules:[15],inclusive:!1},acc_title:{rules:[13],inclusive:!1},INITIAL:{rules:[0,5,6,7,8,9,10,11,12,14,16,19,20,21,22,23,24],inclusive:!0}}};function d(){this.yy={}}return y.lexer=p,d.prototype=y,y.Parser=d,new d}());a.parser=a;const o=a;let c="";const l=[],h=[],u=[],y=function(){let t=!0;for(const[e,n]of u.entries())u[e].processed,t=t&&n.processed;return t},p={parseDirective:function(t,e,n){i.m.parseDirective(this,t,e,n)},getConfig:()=>(0,i.c)().journey,clear:function(){l.length=0,h.length=0,c="",u.length=0,(0,i.v)()},setDiagramTitle:i.r,getDiagramTitle:i.t,setAccTitle:i.s,getAccTitle:i.g,setAccDescription:i.b,getAccDescription:i.a,addSection:function(t){c=t,l.push(t)},getSections:function(){return l},getTasks:function(){let t=y();let e=0;for(;!t&&e<100;)t=y(),e++;return h.push(...u),h},addTask:function(t,e){const n=e.substr(1).split(":");let i=0,s=[];1===n.length?(i=Number(n[0]),s=[]):(i=Number(n[0]),s=n[1].split(","));const r=s.map((t=>t.trim())),a={section:c,type:c,people:r,task:t,score:i};u.push(a)},addTaskOrg:function(t){const e={section:c,type:c,description:t,task:t,classes:[]};h.push(e)},getActors:function(){return function(){const t=[];return h.forEach((e=>{e.people&&t.push(...e.people)})),[...new Set(t)].sort()}()}},d=t=>`.label {\n    font-family: 'trebuchet ms', verdana, arial, sans-serif;\n    font-family: var(--mermaid-font-family);\n    color: ${t.textColor};\n  }\n  .mouth {\n    stroke: #666;\n  }\n\n  line {\n    stroke: ${t.textColor}\n  }\n\n  .legend {\n    fill: ${t.textColor};\n  }\n\n  .label text {\n    fill: #333;\n  }\n  .label {\n    color: ${t.textColor}\n  }\n\n  .face {\n    ${t.faceColor?`fill: ${t.faceColor}`:"fill: #FFF8DC"};\n    stroke: #999;\n  }\n\n  .node rect,\n  .node circle,\n  .node ellipse,\n  .node polygon,\n  .node path {\n    fill: ${t.mainBkg};\n    stroke: ${t.nodeBorder};\n    stroke-width: 1px;\n  }\n\n  .node .label {\n    text-align: center;\n  }\n  .node.clickable {\n    cursor: pointer;\n  }\n\n  .arrowheadPath {\n    fill: ${t.arrowheadColor};\n  }\n\n  .edgePath .path {\n    stroke: ${t.lineColor};\n    stroke-width: 1.5px;\n  }\n\n  .flowchart-link {\n    stroke: ${t.lineColor};\n    fill: none;\n  }\n\n  .edgeLabel {\n    background-color: ${t.edgeLabelBackground};\n    rect {\n      opacity: 0.5;\n    }\n    text-align: center;\n  }\n\n  .cluster rect {\n  }\n\n  .cluster text {\n    fill: ${t.titleColor};\n  }\n\n  div.mermaidTooltip {\n    position: absolute;\n    text-align: center;\n    max-width: 200px;\n    padding: 2px;\n    font-family: 'trebuchet ms', verdana, arial, sans-serif;\n    font-family: var(--mermaid-font-family);\n    font-size: 12px;\n    background: ${t.tertiaryColor};\n    border: 1px solid ${t.border2};\n    border-radius: 2px;\n    pointer-events: none;\n    z-index: 100;\n  }\n\n  .task-type-0, .section-type-0  {\n    ${t.fillType0?`fill: ${t.fillType0}`:""};\n  }\n  .task-type-1, .section-type-1  {\n    ${t.fillType0?`fill: ${t.fillType1}`:""};\n  }\n  .task-type-2, .section-type-2  {\n    ${t.fillType0?`fill: ${t.fillType2}`:""};\n  }\n  .task-type-3, .section-type-3  {\n    ${t.fillType0?`fill: ${t.fillType3}`:""};\n  }\n  .task-type-4, .section-type-4  {\n    ${t.fillType0?`fill: ${t.fillType4}`:""};\n  }\n  .task-type-5, .section-type-5  {\n    ${t.fillType0?`fill: ${t.fillType5}`:""};\n  }\n  .task-type-6, .section-type-6  {\n    ${t.fillType0?`fill: ${t.fillType6}`:""};\n  }\n  .task-type-7, .section-type-7  {\n    ${t.fillType0?`fill: ${t.fillType7}`:""};\n  }\n\n  .actor-0 {\n    ${t.actor0?`fill: ${t.actor0}`:""};\n  }\n  .actor-1 {\n    ${t.actor1?`fill: ${t.actor1}`:""};\n  }\n  .actor-2 {\n    ${t.actor2?`fill: ${t.actor2}`:""};\n  }\n  .actor-3 {\n    ${t.actor3?`fill: ${t.actor3}`:""};\n  }\n  .actor-4 {\n    ${t.actor4?`fill: ${t.actor4}`:""};\n  }\n  .actor-5 {\n    ${t.actor5?`fill: ${t.actor5}`:""};\n  }\n`,f=function(t,e){return(0,r.d)(t,e)},g=function(t,e){const n=t.append("circle");return n.attr("cx",e.cx),n.attr("cy",e.cy),n.attr("class","actor-"+e.pos),n.attr("fill",e.fill),n.attr("stroke",e.stroke),n.attr("r",e.r),void 0!==n.class&&n.attr("class",n.class),void 0!==e.title&&n.append("title").text(e.title),n},x=function(t,e){return(0,r.f)(t,e)};let m=-1;const k=function(){function t(t,e,n,s,r,a,o,c){i(e.append("text").attr("x",n+r/2).attr("y",s+a/2+5).style("font-color",c).style("text-anchor","middle").text(t),o)}function e(t,e,n,s,r,a,o,c,l){const{taskFontSize:h,taskFontFamily:u}=c,y=t.split(/<br\s*\/?>/gi);for(let p=0;p<y.length;p++){const t=p*h-h*(y.length-1)/2,c=e.append("text").attr("x",n+r/2).attr("y",s).attr("fill",l).style("text-anchor","middle").style("font-size",h).style("font-family",u);c.append("tspan").attr("x",n+r/2).attr("dy",t).text(y[p]),c.attr("y",s+a/2).attr("dominant-baseline","central").attr("alignment-baseline","central"),i(c,o)}}function n(t,n,s,r,a,o,c,l){const h=n.append("switch"),u=h.append("foreignObject").attr("x",s).attr("y",r).attr("width",a).attr("height",o).attr("position","fixed").append("xhtml:div").style("display","table").style("height","100%").style("width","100%");u.append("div").attr("class","label").style("display","table-cell").style("text-align","center").style("vertical-align","middle").text(t),e(t,h,s,r,a,o,c,l),i(u,c)}function i(t,e){for(const n in e)n in e&&t.attr(n,e[n])}return function(i){return"fo"===i.textPlacement?n:"old"===i.textPlacement?t:e}}(),_=g,v=function(t,e,n){const i=t.append("g"),s=(0,r.g)();s.x=e.x,s.y=e.y,s.fill=e.fill,s.width=n.width*e.taskCount+n.diagramMarginX*(e.taskCount-1),s.height=n.height,s.class="journey-section section-type-"+e.num,s.rx=3,s.ry=3,f(i,s),k(n)(e.text,i,s.x,s.y,s.width,s.height,{class:"journey-section section-type-"+e.num},n,e.colour)},b=x,$=function(t,e,n){const i=e.x+n.width/2,a=t.append("g");m++;a.append("line").attr("id","task"+m).attr("x1",i).attr("y1",e.y).attr("x2",i).attr("y2",450).attr("class","task-line").attr("stroke-width","1px").attr("stroke-dasharray","4 2").attr("stroke","#666"),function(t,e){const n=15,i=t.append("circle").attr("cx",e.cx).attr("cy",e.cy).attr("class","face").attr("r",n).attr("stroke-width",2).attr("overflow","visible"),r=t.append("g");r.append("circle").attr("cx",e.cx-5).attr("cy",e.cy-5).attr("r",1.5).attr("stroke-width",2).attr("fill","#666").attr("stroke","#666"),r.append("circle").attr("cx",e.cx+5).attr("cy",e.cy-5).attr("r",1.5).attr("stroke-width",2).attr("fill","#666").attr("stroke","#666"),e.score>3?function(t){const i=(0,s.JLW)().startAngle(Math.PI/2).endAngle(Math.PI/2*3).innerRadius(7.5).outerRadius(n/2.2);t.append("path").attr("class","mouth").attr("d",i).attr("transform","translate("+e.cx+","+(e.cy+2)+")")}(r):e.score<3?function(t){const i=(0,s.JLW)().startAngle(3*Math.PI/2).endAngle(Math.PI/2*5).innerRadius(7.5).outerRadius(n/2.2);t.append("path").attr("class","mouth").attr("d",i).attr("transform","translate("+e.cx+","+(e.cy+7)+")")}(r):r.append("line").attr("class","mouth").attr("stroke",2).attr("x1",e.cx-5).attr("y1",e.cy+7).attr("x2",e.cx+5).attr("y2",e.cy+7).attr("class","mouth").attr("stroke-width","1px").attr("stroke","#666")}(a,{cx:i,cy:300+30*(5-e.score),score:e.score});const o=(0,r.g)();o.x=e.x,o.y=e.y,o.fill=e.fill,o.width=n.width,o.height=n.height,o.class="task task-type-"+e.num,o.rx=3,o.ry=3,f(a,o);let c=e.x+14;e.people.forEach((t=>{const n=e.actors[t].color,i={cx:c,cy:e.y,r:7,fill:n,stroke:"#000",title:t,pos:e.actors[t].position};g(a,i),c+=10})),k(n)(e.task,a,o.x,o.y,o.width,o.height,{class:"task"},n,e.colour)},w=function(t){t.append("defs").append("marker").attr("id","arrowhead").attr("refX",5).attr("refY",2).attr("markerWidth",6).attr("markerHeight",4).attr("orient","auto").append("path").attr("d","M 0,0 V 4 L6,2 Z")},M={};const E=(0,i.c)().journey,S=E.leftMargin,T={data:{startx:void 0,stopx:void 0,starty:void 0,stopy:void 0},verticalPos:0,sequenceItems:[],init:function(){this.sequenceItems=[],this.data={startx:void 0,stopx:void 0,starty:void 0,stopy:void 0},this.verticalPos=0},updateVal:function(t,e,n,i){void 0===t[e]?t[e]=n:t[e]=i(n,t[e])},updateBounds:function(t,e,n,s){const r=(0,i.c)().journey,a=this;let o=0;var c;this.sequenceItems.forEach((function(i){o++;const l=a.sequenceItems.length-o+1;a.updateVal(i,"starty",e-l*r.boxMargin,Math.min),a.updateVal(i,"stopy",s+l*r.boxMargin,Math.max),a.updateVal(T.data,"startx",t-l*r.boxMargin,Math.min),a.updateVal(T.data,"stopx",n+l*r.boxMargin,Math.max),"activation"!==c&&(a.updateVal(i,"startx",t-l*r.boxMargin,Math.min),a.updateVal(i,"stopx",n+l*r.boxMargin,Math.max),a.updateVal(T.data,"starty",e-l*r.boxMargin,Math.min),a.updateVal(T.data,"stopy",s+l*r.boxMargin,Math.max))}))},insert:function(t,e,n,i){const s=Math.min(t,n),r=Math.max(t,n),a=Math.min(e,i),o=Math.max(e,i);this.updateVal(T.data,"startx",s,Math.min),this.updateVal(T.data,"starty",a,Math.min),this.updateVal(T.data,"stopx",r,Math.max),this.updateVal(T.data,"stopy",o,Math.max),this.updateBounds(s,a,r,o)},bumpVerticalPos:function(t){this.verticalPos=this.verticalPos+t,this.data.stopy=this.verticalPos},getVerticalPos:function(){return this.verticalPos},getBounds:function(){return this.data}},A=E.sectionFills,I=E.sectionColours,P=function(t,e,n){const s=(0,i.c)().journey;let r="";const a=n+(2*s.height+s.diagramMarginY);let o=0,c="#CCC",l="black",h=0;for(const[i,u]of e.entries()){if(r!==u.section){c=A[o%A.length],h=o%A.length,l=I[o%I.length];let n=0;const a=u.section;for(let t=i;t<e.length&&e[t].section==a;t++)n+=1;const y={x:i*s.taskMargin+i*s.width+S,y:50,text:u.section,fill:c,num:h,colour:l,taskCount:n};v(t,y,s),r=u.section,o++}const n=u.people.reduce(((t,e)=>(M[e]&&(t[e]=M[e]),t)),{});u.x=i*s.taskMargin+i*s.width+S,u.y=a,u.width=s.diagramMarginX,u.height=s.diagramMarginY,u.colour=l,u.fill=c,u.num=h,u.actors=n,$(t,u,s),T.insert(u.x,u.y,u.x+u.width+s.taskMargin,450)}},C={setConf:function(t){Object.keys(t).forEach((function(e){E[e]=t[e]}))},draw:function(t,e,n,r){const a=(0,i.c)().journey;r.db.clear(),r.parser.parse(t+"\n");const o=(0,i.c)().securityLevel;let c;"sandbox"===o&&(c=(0,s.Ltv)("#i"+e));const l="sandbox"===o?(0,s.Ltv)(c.nodes()[0].contentDocument.body):(0,s.Ltv)("body");T.init();const h=l.select("#"+e);w(h);const u=r.db.getTasks(),y=r.db.getDiagramTitle(),p=r.db.getActors();for(const i in M)delete M[i];let d=0;p.forEach((t=>{M[t]={color:a.actorColours[d%a.actorColours.length],position:d},d++})),function(t){const e=(0,i.c)().journey;let n=60;Object.keys(M).forEach((i=>{const s=M[i].color,r={cx:20,cy:n,r:7,fill:s,stroke:"#000",pos:M[i].position};_(t,r);const a={x:40,y:n+7,fill:"#666",text:i,textMargin:5|e.boxTextMargin};b(t,a),n+=20}))}(h),T.insert(0,0,S,50*Object.keys(M).length),P(h,u,0);const f=T.getBounds();y&&h.append("text").text(y).attr("x",S).attr("font-size","4ex").attr("font-weight","bold").attr("y",25);const g=f.stopy-f.starty+2*a.diagramMarginY,x=S+f.stopx+2*a.diagramMarginX;(0,i.i)(h,g,x,a.useMaxWidth),h.append("line").attr("x1",S).attr("y1",4*a.height).attr("x2",x-S-4).attr("y2",4*a.height).attr("stroke-width",4).attr("stroke","black").attr("marker-end","url(#arrowhead)");const m=y?70:0;h.attr("viewBox",`${f.startx} -25 ${x} ${g+m}`),h.attr("preserveAspectRatio","xMinYMin meet"),h.attr("height",g+m+25)}},D={parser:o,db:p,renderer:C,styles:d,init:t=>{C.setConf(t.journey),p.clear()}}},2516:(t,e,n)=>{n.d(e,{a:()=>r,b:()=>c,c:()=>o,d:()=>s,e:()=>h,f:()=>a,g:()=>l});var i=n(6750);const s=function(t,e){const n=t.append("rect");if(n.attr("x",e.x),n.attr("y",e.y),n.attr("fill",e.fill),n.attr("stroke",e.stroke),n.attr("width",e.width),n.attr("height",e.height),n.attr("rx",e.rx),n.attr("ry",e.ry),"undefined"!==e.attrs&&null!==e.attrs)for(let i in e.attrs)n.attr(i,e.attrs[i]);return"undefined"!==e.class&&n.attr("class",e.class),n},r=function(t,e){s(t,{x:e.startx,y:e.starty,width:e.stopx-e.startx,height:e.stopy-e.starty,fill:e.fill,stroke:e.stroke,class:"rect"}).lower()},a=function(t,e){const n=e.text.replace(/<br\s*\/?>/gi," "),i=t.append("text");i.attr("x",e.x),i.attr("y",e.y),i.attr("class","legend"),i.style("text-anchor",e.anchor),void 0!==e.class&&i.attr("class",e.class);const s=i.append("tspan");return s.attr("x",e.x+2*e.textMargin),s.text(n),i},o=function(t,e,n,s){const r=t.append("image");r.attr("x",e),r.attr("y",n);var a=(0,i.J)(s);r.attr("xlink:href",a)},c=function(t,e,n,s){const r=t.append("use");r.attr("x",e),r.attr("y",n);const a=(0,i.J)(s);r.attr("xlink:href","#"+a)},l=function(){return{x:0,y:0,width:100,height:100,fill:"#EDF2AE",stroke:"#666",anchor:"start",rx:0,ry:0}},h=function(){return{x:0,y:0,width:100,height:100,fill:void 0,anchor:void 0,"text-anchor":"start",style:"#666",textMargin:0,rx:0,ry:0,tspan:!0,valign:void 0}}}}]);