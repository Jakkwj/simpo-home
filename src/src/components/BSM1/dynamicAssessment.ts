// Days 7–14. Full-precision comparison values and signed contributions accompany /files/bsm1/Assessment.csv.
export default [
  {
    "id": "03",
    "en": "Dry, open",
    "zh": "晴天开环",
    "readings": [
      {
        "metric": "EQ",
        "report": 6690.1066,
        "matlab": 6690.104899179579,
        "tight": 6690.143421328654,
        "saved": 6690.330605210541,
        "en": "At the same tolerance, the gap before correcting the input times was +0.05008. Effluent concentrations now contribute +0.03882 and flow contributes −0.00029. Ammonium contributes +0.05254 at a weight of 30. Nitrate offsets 0.01738 at a weight of 10.",
        "zh": "校正输入时刻前，相同容差下的差值为 +0.05008。目前，出水浓度和出水流量分别贡献 +0.03882 和 −0.00029。氨氮的权重为 30，贡献 +0.05254，硝态氮的权重为 10，抵消其中 0.01738。"
      },
      {
        "metric": "SP",
        "report": 2435.6901,
        "matlab": 2435.6899912694475,
        "tight": 2435.7041676662307,
        "saved": 2435.696858856672,
        "en": "On the same rerun, selecting 23:45 for the closing stock moves SP by +0.12980 kg SS/d relative to midnight. With matching endpoints, daily wastage contributes +0.00768. The difference in inventory change is +0.0455 kg, or +0.00650 kg SS/d.",
        "zh": "同一条新轨迹，期末库存从午夜改取 23:45，SP 改变 +0.12980 kg SS/d。与 MATLAB 取同一条记录后，日均排泥量差为 +0.00768，两边库存变化量相差 +0.0455 kg，摊到每天为 +0.00650 kg SS/d。"
      },
      {
        "metric": "AE",
        "report": 3341.3867,
        "matlab": 3341.386666666668,
        "tight": 3341.386666666668,
        "saved": 3341.386666666668,
        "en": "",
        "zh": ""
      },
      {
        "metric": "PE",
        "report": 388.17,
        "matlab": 388.17000000000024,
        "tight": 388.17000000000024,
        "saved": 388.17000000000024,
        "en": "",
        "zh": ""
      },
      {
        "metric": "EC",
        "report": 0.0,
        "matlab": 0.0,
        "tight": 0.0,
        "saved": 0.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "ME",
        "report": 240.0,
        "matlab": 240.0,
        "tight": 240.0,
        "saved": 240.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "OCI",
        "report": 16148.0073,
        "matlab": 16148.006623013907,
        "tight": 16148.07750499782,
        "saved": 16148.04096095003,
        "en": "The sludge-disposal weight of five converts the residual SP difference into +0.07088 index points.",
        "zh": "污泥处置权重为 5。两边 SP 的余差乘以 5，贡献 +0.07088 个指数点。"
      }
    ]
  },
  {
    "id": "04",
    "en": "Dry, closed",
    "zh": "晴天闭环",
    "readings": [
      {
        "metric": "EQ",
        "report": 6123.0182,
        "matlab": 6123.018194875287,
        "tight": 6123.027665572723,
        "saved": 6123.105095455953,
        "en": "At the same tolerance, the gap before correcting the input times was +0.01950. Effluent concentrations now contribute +0.00842 and flow contributes +0.00105. Ammonium contributes +0.01231 at a weight of 30. Nitrate offsets 0.00420 at a weight of 10.",
        "zh": "校正输入时刻前，相同容差下的差值为 +0.01950。目前，出水浓度和出水流量分别贡献 +0.00842 和 +0.00105。氨氮的权重为 30，贡献 +0.01231，硝态氮的权重为 10，抵消其中 0.00420。"
      },
      {
        "metric": "SP",
        "report": 2440.6057,
        "matlab": 2440.6056436010967,
        "tight": 2440.606934075352,
        "saved": 2440.609414488328,
        "en": "On the same rerun, selecting 23:45 for the closing stock moves SP by +0.03465 kg SS/d relative to midnight. With matching endpoints, daily wastage contributes +0.00066. The difference in inventory change is +0.0044 kg, or +0.00063 kg SS/d.",
        "zh": "同一条新轨迹，期末库存从午夜改取 23:45，SP 改变 +0.03465 kg SS/d。与 MATLAB 取同一条记录后，日均排泥量差为 +0.00066，两边库存变化量相差 +0.0044 kg，摊到每天为 +0.00063 kg SS/d。"
      },
      {
        "metric": "AE",
        "report": 3698.3438,
        "matlab": 3698.3438443445734,
        "tight": 3698.346410792515,
        "saved": 3698.3505621597615,
        "en": "With aeration fixed in the other tanks, tank 5’s mean applied KLa is 0.000433 d⁻¹ higher than MATLAB over week two. Multiplying this by 8 × 1333 / 1800 gives the aeration-energy difference.",
        "zh": "闭环中，其他池的曝气输入固定。Tank5 在第二周的平均实际 KLa 比 MATLAB 高 0.000433 d⁻¹。代入 8 × 1333 × KLa 差 ÷ 1800，即得到本行曝气能耗差。"
      },
      {
        "metric": "PE",
        "report": 241.0305,
        "matlab": 241.0305076241295,
        "tight": 241.03082141067165,
        "saved": 241.0271625509951,
        "en": "Return and waste flows are fixed. Mean internal recycle is 0.07845 m³/d higher than MATLAB in week two. Its pump coefficient of 0.004 kWh/m³ converts this into the energy difference.",
        "zh": "污泥回流和排泥流量固定。第二周平均内回流量比 MATLAB 高 0.07845 m³/d，乘以内回流单位泵送能耗 0.004 kWh/m³，即得到本行的差值。"
      },
      {
        "metric": "EC",
        "report": 0.0,
        "matlab": 0.0,
        "tight": 0.0,
        "saved": 0.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "ME",
        "report": 240.0,
        "matlab": 240.0,
        "tight": 240.0,
        "saved": 240.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "OCI",
        "report": 16382.4027,
        "matlab": 16382.402569974187,
        "tight": 16382.411902579948,
        "saved": 16382.424797152398,
        "en": "The sludge-disposal weight of five converts the residual SP difference into +0.00645 index points. Aeration adds +0.00257 and pumping +0.00031.",
        "zh": "污泥处置权重为 5。两边 SP 的余差乘以 5，贡献 +0.00645 个指数点。 曝气和泵送再分别贡献 +0.00257 和 +0.00031。"
      }
    ]
  },
  {
    "id": "05",
    "en": "Rain, open",
    "zh": "雨天开环",
    "readings": [
      {
        "metric": "EQ",
        "report": 8951.3288,
        "matlab": 8935.201660559334,
        "tight": 8935.224323885159,
        "saved": 8935.142460124112,
        "en": "At the same tolerance, the gap before correcting the input times was +0.03710. Effluent concentrations now contribute +0.02268 and flow contributes −0.00001. Ammonium contributes +0.03296 at a weight of 30. Nitrate offsets 0.01451 at a weight of 10. The 2008 report exceeds R2024b by 16.13. The cause of that historical difference remains unknown.",
        "zh": "校正输入时刻前，相同容差下的差值为 +0.03710。目前，出水浓度和出水流量分别贡献 +0.02268 和 −0.00001。氨氮的权重为 30，贡献 +0.03296，硝态氮的权重为 10，抵消其中 0.01451。 2008 年原报告比 R2024b 高 16.13，历史差异的原因尚未查明。"
      },
      {
        "metric": "SP",
        "report": 2353.0104,
        "matlab": 2352.447324646602,
        "tight": 2352.4627399277015,
        "saved": 2352.466240953663,
        "en": "On the same rerun, selecting 23:45 for the closing stock moves SP by −0.10844 kg SS/d relative to midnight. With matching endpoints, daily wastage contributes +0.00990. The difference in inventory change is +0.0386 kg, or +0.00551 kg SS/d.",
        "zh": "同一条新轨迹，期末库存从午夜改取 23:45，SP 改变 −0.10844 kg SS/d。与 MATLAB 取同一条记录后，日均排泥量差为 +0.00990，两边库存变化量相差 +0.0386 kg，摊到每天为 +0.00551 kg SS/d。"
      },
      {
        "metric": "AE",
        "report": 3341.3867,
        "matlab": 3341.386666666668,
        "tight": 3341.386666666668,
        "saved": 3341.386666666668,
        "en": "",
        "zh": ""
      },
      {
        "metric": "PE",
        "report": 388.17,
        "matlab": 388.17000000000024,
        "tight": 388.17000000000024,
        "saved": 388.17000000000024,
        "en": "",
        "zh": ""
      },
      {
        "metric": "EC",
        "report": 0.0,
        "matlab": 0.0,
        "tight": 0.0,
        "saved": 0.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "ME",
        "report": 240.0,
        "matlab": 240.0,
        "tight": 240.0,
        "saved": 240.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "OCI",
        "report": 15734.6089,
        "matlab": 15731.793289899679,
        "tight": 15731.870366305177,
        "saved": 15731.887871434983,
        "en": "The sludge-disposal weight of five converts the residual SP difference into +0.07708 index points.",
        "zh": "污泥处置权重为 5。两边 SP 的余差乘以 5，贡献 +0.07708 个指数点。"
      }
    ]
  },
  {
    "id": "06",
    "en": "Rain, closed",
    "zh": "雨天闭环",
    "readings": [
      {
        "metric": "EQ",
        "report": 8184.7263,
        "matlab": 8184.726189590342,
        "tight": 8184.7284040649965,
        "saved": 8184.75903543665,
        "en": "At the same tolerance, the gap before correcting the input times was +0.01575. Effluent concentrations now contribute +0.00349 and flow contributes −0.00127. Ammonium contributes +0.00656 at a weight of 30. Nitrate offsets 0.00372 at a weight of 10.",
        "zh": "校正输入时刻前，相同容差下的差值为 +0.01575。目前，出水浓度和出水流量分别贡献 +0.00349 和 −0.00127。氨氮的权重为 30，贡献 +0.00656，硝态氮的权重为 10，抵消其中 0.00372。"
      },
      {
        "metric": "SP",
        "report": 2357.5863,
        "matlab": 2357.5862542211325,
        "tight": 2357.5883221385748,
        "saved": 2357.5913703896376,
        "en": "On the same rerun, selecting 23:45 for the closing stock moves SP by −0.20846 kg SS/d relative to midnight. With matching endpoints, daily wastage contributes +0.00086. The difference in inventory change is +0.0084 kg, or +0.00120 kg SS/d.",
        "zh": "同一条新轨迹，期末库存从午夜改取 23:45，SP 改变 −0.20846 kg SS/d。与 MATLAB 取同一条记录后，日均排泥量差为 +0.00086，两边库存变化量相差 +0.0084 kg，摊到每天为 +0.00120 kg SS/d。"
      },
      {
        "metric": "AE",
        "report": 3671.3519,
        "matlab": 3671.351885484786,
        "tight": 3671.3541185672593,
        "saved": 3671.3559703255764,
        "en": "With aeration fixed in the other tanks, tank 5’s mean applied KLa is 0.000377 d⁻¹ higher than MATLAB over week two. Multiplying this by 8 × 1333 / 1800 gives the aeration-energy difference.",
        "zh": "闭环中，其他池的曝气输入固定。Tank5 在第二周的平均实际 KLa 比 MATLAB 高 0.000377 d⁻¹。代入 8 × 1333 × KLa 差 ÷ 1800，即得到本行曝气能耗差。"
      },
      {
        "metric": "PE",
        "report": 285.264,
        "matlab": 285.26402144154406,
        "tight": 285.26487185641935,
        "saved": 285.2609688923779,
        "en": "Return and waste flows are fixed. Mean internal recycle is 0.21260 m³/d higher than MATLAB in week two. Its pump coefficient of 0.004 kWh/m³ converts this into the energy difference.",
        "zh": "污泥回流和排泥流量固定。第二周平均内回流量比 MATLAB 高 0.21260 m³/d，乘以内回流单位泵送能耗 0.004 kWh/m³，即得到本行的差值。"
      },
      {
        "metric": "EC",
        "report": 0.0,
        "matlab": 0.0,
        "tight": 0.0,
        "saved": 0.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "ME",
        "report": 240.0,
        "matlab": 240.0,
        "tight": 240.0,
        "saved": 240.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "OCI",
        "report": 15984.5473,
        "matlab": 15984.547178031993,
        "tight": 15984.560601116551,
        "saved": 15984.573791166142,
        "en": "The sludge-disposal weight of five converts the residual SP difference into +0.01034 index points. Aeration adds +0.00223 and pumping +0.00085.",
        "zh": "污泥处置权重为 5。两边 SP 的余差乘以 5，贡献 +0.01034 个指数点。 曝气和泵送再分别贡献 +0.00223 和 +0.00085。"
      }
    ]
  },
  {
    "id": "07",
    "en": "Storm, open",
    "zh": "暴雨开环",
    "readings": [
      {
        "metric": "EQ",
        "report": 8197.7197,
        "matlab": 8021.732680952763,
        "tight": 8021.784792890082,
        "saved": 8021.045659069925,
        "en": "At the same tolerance, the gap before correcting the input times was +0.06377. Effluent concentrations now contribute +0.05240 and flow contributes −0.00029. Ammonium contributes +0.06729 at a weight of 30. Nitrate offsets 0.02010 at a weight of 10. The 2008 report exceeds R2024b by 175.99. The cause of that historical difference remains unknown.",
        "zh": "校正输入时刻前，相同容差下的差值为 +0.06377。目前，出水浓度和出水流量分别贡献 +0.05240 和 −0.00029。氨氮的权重为 30，贡献 +0.06729，硝态氮的权重为 10，抵消其中 0.02010。 2008 年原报告比 R2024b 高 175.99，历史差异的原因尚未查明。"
      },
      {
        "metric": "SP",
        "report": 2607.4907,
        "matlab": 2599.3590389631836,
        "tight": 2599.3748051739053,
        "saved": 2599.441081015422,
        "en": "On the same rerun, selecting 23:45 for the closing stock moves SP by +0.18984 kg SS/d relative to midnight. With matching endpoints, daily wastage contributes +0.00961. The difference in inventory change is +0.0431 kg, or +0.00616 kg SS/d.",
        "zh": "同一条新轨迹，期末库存从午夜改取 23:45，SP 改变 +0.18984 kg SS/d。与 MATLAB 取同一条记录后，日均排泥量差为 +0.00961，两边库存变化量相差 +0.0431 kg，摊到每天为 +0.00616 kg SS/d。"
      },
      {
        "metric": "AE",
        "report": 3341.3867,
        "matlab": 3341.386666666668,
        "tight": 3341.386666666668,
        "saved": 3341.386666666668,
        "en": "",
        "zh": ""
      },
      {
        "metric": "PE",
        "report": 388.17,
        "matlab": 388.17000000000024,
        "tight": 388.17000000000024,
        "saved": 388.17000000000024,
        "en": "",
        "zh": ""
      },
      {
        "metric": "EC",
        "report": 0.0,
        "matlab": 0.0,
        "tight": 0.0,
        "saved": 0.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "ME",
        "report": 240.0,
        "matlab": 240.0,
        "tight": 240.0,
        "saved": 240.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "OCI",
        "report": 17007.0104,
        "matlab": 16966.351861482588,
        "tight": 16966.430692536196,
        "saved": 16966.76207174378,
        "en": "The sludge-disposal weight of five converts the residual SP difference into +0.07883 index points.",
        "zh": "污泥处置权重为 5。两边 SP 的余差乘以 5，贡献 +0.07883 个指数点。"
      }
    ]
  },
  {
    "id": "08",
    "en": "Storm, closed",
    "zh": "暴雨闭环",
    "readings": [
      {
        "metric": "EQ",
        "report": 7220.7241,
        "matlab": 7220.724005998308,
        "tight": 7220.734330981768,
        "saved": 7220.767499539579,
        "en": "At the same tolerance, the gap before correcting the input times was +0.02018. Effluent concentrations now contribute +0.00863 and flow contributes +0.00170. Ammonium contributes +0.01363 at a weight of 30. Nitrate offsets 0.00596 at a weight of 10.",
        "zh": "校正输入时刻前，相同容差下的差值为 +0.02018。目前，出水浓度和出水流量分别贡献 +0.00863 和 +0.00170。氨氮的权重为 30，贡献 +0.01363，硝态氮的权重为 10，抵消其中 0.00596。"
      },
      {
        "metric": "SP",
        "report": 2605.4902,
        "matlab": 2605.490133211447,
        "tight": 2605.4934475787218,
        "saved": 2605.492073719987,
        "en": "On the same rerun, selecting 23:45 for the closing stock moves SP by +0.07577 kg SS/d relative to midnight. With matching endpoints, daily wastage contributes +0.00142. The difference in inventory change is +0.0133 kg, or +0.00189 kg SS/d.",
        "zh": "同一条新轨迹，期末库存从午夜改取 23:45，SP 改变 +0.07577 kg SS/d。与 MATLAB 取同一条记录后，日均排泥量差为 +0.00142，两边库存变化量相差 +0.0133 kg，摊到每天为 +0.00189 kg SS/d。"
      },
      {
        "metric": "AE",
        "report": 3720.9173,
        "matlab": 3720.9173515603957,
        "tight": 3720.920434826875,
        "saved": 3720.9241101708913,
        "en": "With aeration fixed in the other tanks, tank 5’s mean applied KLa is 0.000520 d⁻¹ higher than MATLAB over week two. Multiplying this by 8 × 1333 / 1800 gives the aeration-energy difference.",
        "zh": "闭环中，其他池的曝气输入固定。Tank5 在第二周的平均实际 KLa 比 MATLAB 高 0.000520 d⁻¹。代入 8 × 1333 × KLa 差 ÷ 1800，即得到本行曝气能耗差。"
      },
      {
        "metric": "PE",
        "report": 265.1984,
        "matlab": 265.1983743615368,
        "tight": 265.1995923066112,
        "saved": 265.1959103604307,
        "en": "Return and waste flows are fixed. Mean internal recycle is 0.30449 m³/d higher than MATLAB in week two. Its pump coefficient of 0.004 kWh/m³ converts this into the energy difference.",
        "zh": "污泥回流和排泥流量固定。第二周平均内回流量比 MATLAB 高 0.30449 m³/d，乘以内回流单位泵送能耗 0.004 kWh/m³，即得到本行的差值。"
      },
      {
        "metric": "EC",
        "report": 0.0,
        "matlab": 0.0,
        "tight": 0.0,
        "saved": 0.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "ME",
        "report": 240.0,
        "matlab": 240.0,
        "tight": 240.0,
        "saved": 240.0,
        "en": "",
        "zh": ""
      },
      {
        "metric": "OCI",
        "report": 17253.5665,
        "matlab": 17253.566391979166,
        "tight": 17253.587265027094,
        "saved": 17253.580389131257,
        "en": "The sludge-disposal weight of five converts the residual SP difference into +0.01657 index points. Aeration adds +0.00308 and pumping +0.00122.",
        "zh": "污泥处置权重为 5。两边 SP 的余差乘以 5，贡献 +0.01657 个指数点。 曝气和泵送再分别贡献 +0.00308 和 +0.00122。"
      }
    ]
  }
];
