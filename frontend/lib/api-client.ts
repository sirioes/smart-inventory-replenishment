import type {
  DashboardResponse,
  ForecastHistoryResponse,
  ForecastResponse,
  HealthResponse,
  ReorderRecommendationResponse,
} from "@/types/api";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  readonly status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${BASE_URL}${path}`, {
      ...init,
      headers: {
        Accept: "application/json",
        ...(init?.body ? { "Content-Type": "application/json" } : {}),
        ...init?.headers,
      },
      cache: "no-store",
    });
  } catch {
    throw new ApiError(0, `Could not reach the API at ${BASE_URL}${path}`);
  }

  if (!response.ok) {
    const detail = await response
      .json()
      .then((body: { detail?: string }) => body.detail)
      .catch(() => undefined);
    throw new ApiError(response.status, detail ?? response.statusText);
  }

  return response.json() as Promise<T>;
}

export function getHealth(): Promise<HealthResponse> {
  return request<HealthResponse>("/health");
}

export function getDashboardData(): Promise<DashboardResponse> {
  return request<DashboardResponse>("/dashboard");
}

export function getForecastHistory(
  productId: string,
): Promise<ForecastHistoryResponse> {
  return request<ForecastHistoryResponse>(
    `/products/${encodeURIComponent(productId)}/forecasts`,
  );
}

export function processProduct(
  productId: string,
): Promise<ReorderRecommendationResponse> {
  return request<ReorderRecommendationResponse>(
    `/products/${encodeURIComponent(productId)}/process`,
    { method: "POST" },
  );
}

export function triggerForecast(productId: string): Promise<ForecastResponse> {
  return request<ForecastResponse>(
    `/products/${encodeURIComponent(productId)}/forecast`,
    { method: "POST" },
  );
}
