from typing import List


from esi_formats.esi_classes import market_item_history

stage_1_escalation : List[market_item_history] = [
    market_item_history(item="Miner II", region_name="Outer Passage", required_qty= 40, market_history= []),
    market_item_history(item="150mm Railgun II", region_name="Outer Passage", required_qty= 150, market_history= []),
    market_item_history(item="Gravimetric ECM II", region_name="Outer Passage", required_qty= 100, market_history= []),
    market_item_history(item="Ladar ECM II", region_name="Outer Passage", required_qty= 100, market_history= []),
    market_item_history(item="Magnetometric ECM II", region_name="Outer Passage", required_qty= 100, market_history= []),
    market_item_history(item="Multispectral ECM II", region_name="Outer Passage", required_qty= 100, market_history= []),
    market_item_history(item="Radar ECM II", region_name="Outer Passage", required_qty= 100, market_history= []),
    market_item_history(item="Remote Sensor Dampener II", region_name="Outer Passage", required_qty= 150, market_history= []),
    market_item_history(item="Stasis Webifier II", region_name="Outer Passage", required_qty= 150, market_history= []),
    market_item_history(item="Target Painter II", region_name="Outer Passage", required_qty= 100, market_history= []),
    market_item_history(item="Warp Disruptor II", region_name="Outer Passage", required_qty= 150, market_history= []),
    market_item_history(item="Warp Scrambler II", region_name="Outer Passage", required_qty= 150, market_history= []),
    market_item_history(item="Sensor Booster II", region_name="Outer Passage", required_qty= 100, market_history= []),
    market_item_history(item="Medium Capacitor Booster II", region_name="Outer Passage", required_qty= 20, market_history= []),
    market_item_history(item="Muninn", region_name="Outer Passage", required_qty= 40, market_history= []),
    market_item_history(item="720mm Howitzer Artillery II", region_name="Outer Passage", required_qty= 300, market_history= [])
]
stage_1_supply = [
    ["Capacitor Power Relay II", 150],
    ["Damage Control II", 500],
    ["50MN Quad LiF Restrained Microwarpdrive", 250],
    ["Multispectrum Shield Hardener II",150],
    ["Large Remote Shield Booster II", 150],
    ["Medium Remote Shield Booster II", 150],
    ["Large Remote Shield Booster II", 150],
    ["Medium Core Defense Field Extender II", 150],
    ["Acolyte II ", 400],
    ["Hornet EC-300", 150],
    ["Nanite Repair Paste", 50000],
    ["Standard Mindflood Booster", 150],
    ["Power Diagnostic System II", 300],
    ["Large Remote Shield Booster II", 150],
    ["10MN Afterburner II ", 300],
    ["Kinetic Shield Hardener II", 150],
    ["Nanofiber Internal Structure II", 150],
    ["Large Remote Shield Booster II", 150],
    ["Multispectrum Shield Hardener II", 150],
    ["Prototype Cloaking Device I", 150],
    ["125mm Gatling AutoCannon II", 150],
    ["Small Hyperspatial Velocity Optimizer II", 150],
    ["Republic Fleet EMP S", 150000],
    ["Republic Fleet Depleted Uranium S", 150000],
    ["Large S95a Scoped Remote Shield Booster", 150],
    ["Large Inductive Compact Remote Capacitor Transmitter", 100],
    ["Large Murky Compact Remote Shield Booster", 100],
    ["Warrior II", 2000],
    ["Standard Mindflood Booster", 250],
    ["Large Remote Shield Booster II", 150],
    ]

for i in stage_1_supply:
    stage_1_escalation.append(market_item_history(item = i[0],  region_name= "Outer Passage", required_qty=i[1], market_history= []))

pass