export type UploadTransaction = {
  transaction_date: string | null;
  title: string;
  amount: string;
  entry_type: 'expense' | 'income';
  category_name: string | null;
};

export type UploadResponse = {
  statement_id: number;
  file_name: string;
  file_type: string;
  status: string;
  parser_type: 'csv' | 'pdf';
  summary: string;
  total_transactions: number;
  imported_expenses: number;
  imported_incomes: number;
  total_amount: string;
  transactions: UploadTransaction[];
  used_pdf_extraction: boolean;
};

export type UploadStatement = {
  id: number;
  file_name: string;
  file_type: string;
  upload_status: string;
  parsed_summary: string | null;
  created_at: string;
  processed_at: string | null;
};
