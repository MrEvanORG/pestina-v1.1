document.addEventListener("DOMContentLoaded", function () {
    const box = document.getElementById("priceBox");
    const weightInput = document.getElementById("weightInput");
    const productCostText = document.getElementById("productCostText");
    const shippingCostText = document.getElementById("shippingCostText");
    const totalPriceText = document.getElementById("totalPriceText");
    const errorMessage = document.getElementById("errorMessage");

    const pricePerKg = parseInt(box.dataset.price);
    const shippingCost = parseInt(box.dataset.shipping);
    const minOrder = box.dataset.min ? parseFloat(box.dataset.min) : null;
    const maxOrder = box.dataset.max ? parseFloat(box.dataset.max) : null;

    function fetchFormattedPrice(amount) {
        // ارسال به سرور جهت دریافت فرمت فارسی (اختیاری)
        return fetch(`/format-price/${amount}/`)
            .then(res => res.text())
            .catch(() => `${amount} تومان`);
    }

    weightInput.addEventListener("input", async function () {
        const weight = parseFloat(weightInput.value);
        if (isNaN(weight) || weight <= 0) {
            productCostText.textContent = "";
            totalPriceText.textContent = "";
            errorMessage.textContent = "";
            return;
        }

        if (minOrder !== null && weight < minOrder) {
            errorMessage.textContent = `حداقل سفارش ${minOrder} کیلوگرم است.`;
            return;
        }
        if (maxOrder !== null && weight > maxOrder) {
            errorMessage.textContent = `حداکثر سفارش ${maxOrder} کیلوگرم است.`;
            return;
        }

        errorMessage.textContent = "";

        const productCost = Math.round(weight * pricePerKg);
        const total = productCost + shippingCost;

        // دریافت فرمت فارسی از سرور
        const productFormatted = await fetchFormattedPrice(productCost);
        const totalFormatted = await fetchFormattedPrice(total);

        productCostText.textContent = productFormatted;
        totalPriceText.textContent = totalFormatted;
    });
});
