export interface HealthResponse {
  status: string;
  timestamp: string;
}

export interface ReorderRecommendationResponse {
  product_id: string;
  reorder_point: number;
  recommended_qty: number;
  needs_restock: boolean;
}

export interface ForecastResponse {
  product_id: string;
  predicted_demand: number;
  model_version: string;
  forecast_date: string | null;
}

export interface ProductDashboardItem {
  product_id: string;
  sku: string;
  name: string;
  current_stock: number;
  safety_stock: number;
  reorder_point: number | null;
  recommended_qty: number | null;
  needs_restock: boolean;
  open_alert_count: number;
}

export interface DashboardResponse {
  products: ProductDashboardItem[];
  generated_at: string;
}

export type ForecastHistoryResponse = ForecastResponse[];

export interface SalesHistoryItem {
  transaction_date: string;
  quantity_sold: number;
  is_promo: boolean;
}
