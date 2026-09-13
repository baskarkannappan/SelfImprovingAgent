from self_improving_agent.memory.database import get_connection

def run_strategy_comparison_test() -> str:
    """Run a simulated comparison or simply pull the aggregated stats to output as a report."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, task_type FROM strategies")
        strategies = cursor.fetchall()
        
        report = "## Strategy Comparison Report\n\n"
        
        for strat in strategies:
            strat_id = strat["id"]
            cursor.execute("""
                SELECT 
                    COUNT(*) as sample_count,
                    SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) as success_count,
                    AVG(duration_ms) as avg_duration_ms
                FROM strategy_performance
                WHERE strategy_id = ?
            """, (strat_id,))
            perf = cursor.fetchone()
            
            if perf and perf["sample_count"] > 0:
                success_rate = (perf["success_count"] / perf["sample_count"]) * 100
                report += f"### {strat['name']} ({strat['task_type']})\n"
                report += f"- **Executions**: {perf['sample_count']}\n"
                report += f"- **Success Rate**: {success_rate:.1f}%\n"
                report += f"- **Avg Duration**: {perf['avg_duration_ms']:.0f} ms\n\n"
            else:
                report += f"### {strat['name']} ({strat['task_type']})\n"
                report += f"- No execution data available yet.\n\n"
                
        # Also list preferences
        cursor.execute("SELECT task_type, strategy_id, score, confidence FROM strategy_preferences ORDER BY score DESC")
        prefs = cursor.fetchall()
        if prefs:
            report += "### Current Preferences (Exploitation)\n"
            for p in prefs:
                report += f"- **{p['task_type']}**: `{p['strategy_id']}` (Score: {p['score']:.2f}, Confidence: {p['confidence']})\n"
                
        return report
    except Exception as e:
        return f"Error running comparison: {e}"
    finally:
        conn.close()
