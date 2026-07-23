export type ForecastRequest = {
  months_ahead?: number;
};

export type ForecastItem = {
  month: string;
  predicted_expense: number;
};

export type ExpenseForecastResponse = {
  model_name: string;
  training_points: number;
  last_month_actual: number | null;
  next_month_prediction: number;
  forecast: ForecastItem[];
  method: 'linear_regression' | 'moving_average' | 'no_history';
  confidence: 'low' | 'medium' | 'high';
  message: string;
};
