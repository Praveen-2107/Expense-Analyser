type SpendingTrendChartProps = {
  data: ReadonlyArray<{
    month: string;
    amount: number;
  }>;
};

export function SpendingTrendChart({ data }: SpendingTrendChartProps) {
  const maxAmount = Math.max(...data.map((entry) => entry.amount));
  const points = data
    .map((entry, index) => {
      const x = data.length === 1 ? 0 : (index / (data.length - 1)) * 100;
      const y = 100 - (entry.amount / maxAmount) * 100;
      return `${x},${y}`;
    })
    .join(' ');

  return (
    <div className="analytics-card rounded-4 p-4 p-lg-5 h-100">
      <div className="d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3 mb-4">
        <div>
          <p className="text-uppercase small text-secondary fw-semibold mb-1">Spending Trend</p>
          <h3 className="h4 fw-bold mb-0">Monthly expenditure over time</h3>
        </div>
        <span className="badge rounded-pill text-bg-light border text-secondary px-3 py-2">Last 6 months</span>
      </div>

      <div className="analytics-chart-shell">
        <svg className="analytics-line-chart" viewBox="0 0 100 100" preserveAspectRatio="none" aria-label="Monthly spending trend chart">
          <defs>
            <linearGradient id="trendGradient" x1="0%" y1="0%" x2="0%" y2="100%">
              <stop offset="0%" stopColor="#38bdf8" stopOpacity="0.9" />
              <stop offset="100%" stopColor="#0b5cab" stopOpacity="0.9" />
            </linearGradient>
          </defs>
          <polyline points={points} fill="none" stroke="url(#trendGradient)" strokeWidth="2.8" strokeLinecap="round" strokeLinejoin="round" />
          {data.map((entry, index) => {
            const x = data.length === 1 ? 0 : (index / (data.length - 1)) * 100;
            const y = 100 - (entry.amount / maxAmount) * 100;
            return <circle key={entry.month} cx={x} cy={y} r="1.8" fill="#0b5cab" />;
          })}
        </svg>

        <div className="analytics-axis-labels">
          {data.map((entry) => (
            <span key={entry.month} className="analytics-axis-label">
              {entry.month}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}
