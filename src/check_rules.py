CHECK_RULES = [

    {
        "name": "assets_equation",
        "left": "bsa53",
        "right": ["bsa54", "bsa78"],
        "abs_tolerance": 5000000,
        "relative_tolerance": 1e-5
    },

    {
        "name": "net_sales",
        "left": "isa3",
        "right": ["isa1","isa2"],
        "abs_tolerance": 2000000,
        "relative_tolerance": 1e-5
    },

    {
        "name": "gross_profit",
        "left": "isa5",
        "right": ["isa3","isa4"],
        "abs_tolerance": 2000000,
        "relative_tolerance": 1e-5
    },

    {
        "name": "profit_after_tax",
        "left": "isa20",
        "right": ["isa16","isa19"],
        "abs_tolerance": 2000000,
        "relative_tolerance": 1e-5
    },

    {
        "name": "net_cash_increase",
        "left": "cfa35",
        "right": ["cfa18","cfa26","cfa34"],
        "abs_tolerance": 5000000,
        "relative_tolerance": 1e-5
    },

    {
        "name": "ending_cash",
        "left": "cfa38",
        "right": ["cfa36","cfa35","cfa37"],
        "abs_tolerance": 5000000,
        "relative_tolerance": 1e-5
    },

    {
        "name": "cash_cross_statement",
        "left": "bsa2",
        "right": ["cfa38"],
        "abs_tolerance": 1000000,
        "relative_tolerance": 1e-5
    }

]