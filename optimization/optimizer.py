import pulp

def optimize_bess(df_districts, price_spread=90.0, annual_cycles=365, price_multiplier=1.0):
    """
    Optimizes BESS power (MW) and energy (MWh) for Berlin districts using PuLP,
    incorporating a price sensitivity multiplier for stress testing.
    """
    results = []
    
    for idx, row in df_districts.iterrows():
        district_name = row['neighborhood']
        congestion_factor = row.get('congestion_weight', 1.2)
        
        # Initialize PuLP Linear Programming problem
        prob = pulp.Problem(f"BESS_Optimization_{district_name}", pulp.LpMaximize)
        
        # Decision variables
        power_mw = pulp.LpVariable(f"Power_{district_name}", lowBound=1, upBound=50, cat='Continuous')
        energy_mwh = pulp.LpVariable(f"Energy_{district_name}", lowBound=2, upBound=100, cat='Continuous')
        
        # Constraints: Energy-to-Power ratio (e.g., 2-hour storage duration minimum)
        prob += energy_mwh >= 2 * power_mw
        prob += energy_mwh <= 4 * power_mw
        
        # Objective Function: Maximize Annual Arbitrage Revenue adjusted by Price Multiplier & Congestion
        adjusted_spread = price_spread * price_multiplier
        annual_revenue = power_mw * adjusted_spread * annual_cycles * congestion_factor * 0.001 # scaled
        
        prob += annual_revenue
        
        # Solve the problem
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        
        opt_power = pulp.value(power_mw)
        opt_energy = pulp.value(energy_mwh)
        estimated_profit = pulp.value(annual_revenue) * 1000 # convert back to EUR scale
        
        results.append({
            'neighborhood': district_name,
            'district': row.get('district', 'Berlin'),
            'optimal_bess_mw': round(opt_power, 2),
            'optimal_bess_mwh': round(opt_energy, 2),
            'estimated_annual_profit_eur': int(estimated_profit),
            'congestion_risk': row.get('congestion_risk', 'Medium')
        })
        
    return results
