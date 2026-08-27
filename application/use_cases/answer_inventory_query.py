from domain.interfaces.llm_provider import LLMProvider
from application.use_cases.get_dashboard_data import GetDashboardDataUseCase

SYSTEM_PROMPT_TEMPLATE = (
    "Kamu adalah asisten inventory untuk Smart Inventory Replenishment System. "
    "Jawab pertanyaan HANYA berdasarkan data inventory di bawah ini. "
    "Kalau informasi yang ditanyakan tidak ada di data ini, katakan terus terang "
    "bahwa kamu tidak punya datanya — jangan mengarang angka atau nama produk.\n\n"
    "Data inventory saat ini:\n{context}"
)


class AnswerInventoryQueryUseCase:
    def __init__(
        self,
        llm_provider: LLMProvider,
        dashboard_use_case: GetDashboardDataUseCase,
    ) -> None:
        self.llm_provider = llm_provider
        self.dashboard_use_case = dashboard_use_case

    def execute(self, question: str) -> str:
        products = self.dashboard_use_case.execute()
        system_prompt = SYSTEM_PROMPT_TEMPLATE.format(context=self._build_context(products))
        return self.llm_provider.ask(system_prompt=system_prompt, user_message=question)

    def _build_context(self, products) -> str:
        if not products:
            return "Belum ada produk yang tercatat di sistem."

        lines = []
        for product in products:
            status = "PERLU RESTOCK" if product.needs_restock else "aman"
            line = (
                f"- {product.sku} ({product.name}): stok saat ini {product.current_stock}, "
                f"safety stock {product.safety_stock}, status {status}"
            )
            if product.recommended_qty is not None:
                line += f", rekomendasi qty restock {product.recommended_qty}"
            if product.open_alert_count > 0:
                line += f", {product.open_alert_count} alert terbuka"
            lines.append(line)
        return "\n".join(lines)
