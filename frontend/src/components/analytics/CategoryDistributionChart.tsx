type CategoryDistributionChartProps = {
  items: ReadonlyArray<{
    name: string;
    amount: string;
    percent: number;
    color: string;
  }>;
};

export function CategoryDistributionChart({ items }: CategoryDistributionChartProps) {
  const radius = 42;
  const circumference = 2 * Math.PI * radius;

  let accumulated = 0;

  return (
    <div className="analytics-card rounded-4 p-4 p-lg-5 h-100">
      <p className="text-uppercase small text-secondary fw-semibold mb-1">Category Analytics</p>
      <h3 className="h4 fw-bold mb-4">Where the money goes</h3>

      <div className="d-flex flex-column flex-lg-row align-items-center gap-4 mb-4">
        <div className="donut-chart-wrap position-relative">
          <svg viewBox="0 0 120 120" className="donut-chart" aria-label="Category spending distribution chart">
            <circle cx="60" cy="60" r={radius} className="donut-track" />
            {items.map((item) => {
              const offset = circumference * (accumulated / 100);
              const dashArray = `${circumference * (item.percent / 100)} ${circumference}`;
              accumulated += item.percent;
              return <circle key={item.name} cx="60" cy="60" r={radius} className={`donut-segment ${item.color}`} strokeDasharray={dashArray} strokeDashoffset={-offset} />;
            })}
          </svg>
          <div className="donut-center text-center">
            <p className="text-secondary small mb-1">Total spend</p>
            <h4 className="fw-bold mb-0">$5,280</h4>
          </div>
        </div>

        <div className="flex-grow-1 w-100">
          <div className="d-grid gap-3">
            {items.map((item) => (
              <div key={item.name}>
                <div className="d-flex justify-content-between align-items-center mb-2">
                  <span className="fw-semibold">{item.name}</span>
                  <span className="text-secondary">{item.amount}</span>
                </div>
                <div className="progress budget-progress">
                  <div className={`progress-bar ${item.color}`} style={{ width: `${item.percent}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
