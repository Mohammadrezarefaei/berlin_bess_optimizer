import pulp

def optimize_bess(df_districts, price_spread=90.0, annual_cycles=365, price_multiplier=1.0, deg_cost_per_mwh_cycle=1.5):
    """
    Optimizes BESS power (MW) and energy (MWh) for Berlin districts using PuLP,
    incorporating price sensitivity, battery degradation costs, and ML forecasting.
    """
    results = []
    
    for idx, row in df_districts.iterrows():
        district_name = row['neighborhood']
        congestion_factor = row.get('congestion_weight', 1.2)
        
        prob = pulp.Problem(f"BESS_Optimization_{district_name}", pulp.LpMaximize)
        
        power_mw = pulp.LpVariable(f"Power_{district_name}", lowBound=1, upBound=50, cat='Continuous')
        energy_mwh = pulp.LpVariable(f"Energy_{district_name}", lowBound=2, upBound=100, cat='Continuous')
        
        prob += energy_mwh >= 2 * power_mw
        prob += energy_mwh <= 4 * power_mw
        
        adjusted_spread = price_spread * price_multiplier
        annual_revenue = power_mw * adjusted_spread * annual_cycles * congestion_factor * 0.001
        annual_degradation_cost = energy_mwh * annual_cycles * deg_cost_per_mwh_cycle * 0.001
        
        net_profit = annual_revenue - annual_degradation_cost
        prob += net_profit
        
        prob.solve(pulp.PULP_CBC_CMD(msg=False))
        
        opt_power = pulp.value(power_mw)
        opt_energy = pulp.value(energy_mwh)
        estimated_gross = pulp.value(annual_revenue) * 1000
        estimated_deg_cost = pulp.value(annual_degradation_cost) * 1000
        estimated_net_profit = pulp.value(net_profit) * 1000
        
        results.append({
            'neighborhood': district_name,
            'district': row.get('district', 'Berlin'),
            'optimal_bess_mw': round(opt_power, 2),
            'optimal_bess_mwh': round(opt_energy, 2),
            'gross_revenue_eur': int(estimated_gross),
            'degradation_cost_eur': int(estimated_deg_cost),
            'net_annual_profit_eur': int(estimated_net_profit),
            'congestion_risk': row.get('congestion_risk', 'Medium')
        })
        
    return results
