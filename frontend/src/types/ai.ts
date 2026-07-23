export type AIInsightRequest = {
  focus?: string;
};

export type AIInsightResponse = {
  summary: string;
  insights: string[];
  recommendations: string[];
  used_gemini: boolean;
};
