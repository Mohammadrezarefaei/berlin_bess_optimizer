import pulp
import pandas as pd

def optimize_berlin_bess(gdf, price_spread_eur_per_mwh=80.0, annual_cycles=365):
    """
    مدل بهینه‌سازی خطی با PuLP برای تعیین سایز بهینه و سودآوری BESS در محله‌های برلین
    """
    # ایجاد مسئله بهینه‌سازی (حداکثرسازی سود)
    prob = pulp.LpProblem("Berlin_BESS_Optimization", pulp.LpMaximize)
    
    # متغیرهای تصمیم: ظرفیت توان باتری (MW) برای هر محله
    bess_vars = {}
    for idx, row in gdf.iterrows():
        # متغیر ظرفیت بین 0 تا پتانسیل حداکثر هر محله
        bess_vars[idx] = pulp.LpVariable(f"bess_mw_{row['neighborhood']}", lowBound=0, upBound=row['bess_potential_mw'], cat='Continuous')
    
    # تابع هدف: حداکثر کردن سود سالانه آربیتراژ (فرضیه: درآمد بر اساس اسپرید قیمت و تعداد چرخه)
    # فرض بر این است که هر مگاوات ظرفیت، انرژی معینی را با احتساب راندمان جابجا می‌کند.
    profit_terms = []
    for idx, row in gdf.iterrows():
        # فرض 2 ساعت ذخیره‌سازی (Duration = 2h) برای هر MW ظرفیت توان
        annual_throughput_mwh = bess_vars[idx] * 2 * annual_cycles * 0.85 # با احتساب راندمان RTE
        revenue = annual_throughput_mwh * price_spread_eur_per_mwh
        profit_terms.append(revenue)
        
    prob += pulp.lpSum(profit_terms), "Total_Annual_Profit"
    
    # محدودیت بودجه کل یا ظرفیت تج تج تجمیعی شبکه برلین (مثلاً حداکثر 60 مگاوات در کل شهر)
    max_total_capacity = 60.0
    prob += pulp.lpSum([bess_vars[idx] for idx in gdf.index]) <= max_total_capacity, "Total_Capacity_Limit"
    
    # حل مسئله
    prob.solve(pulp.PULP_CBC_CMD(msg=0))
    
    # استخراج نتایج
    results = []
    for idx, row in gdf.iterrows():
        allocated_mw = pulp.value(bess_vars[idx])
        annual_profit = allocated_mw * 2 * annual_cycles * 0.85 * price_spread_eur_per_mwh
        results.append({
            "neighborhood": row["neighborhood"],
            "district": row["district"],
            "optimal_bess_mw": round(allocated_mw, 2),
            "optimal_bess_mwh": round(allocated_mw * 2, 2),
            "estimated_annual_profit_eur": round(annual_profit, 2),
            "congestion_risk": row["grid_congestion_risk"]
        })
        
    return pd.DataFrame(results)

if __name__ == "__main__":
    from gis.loader import get_berlin_bess_grid_data
    gdf = get_berlin_bess_grid_data()
    df_res = optimize_berlin_bess(gdf)
    print(df_res)