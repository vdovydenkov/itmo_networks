// Получаем IP пользователя
fetch("https://api.ipify.org?format=json")
  .then(response => response.json())
  .then(data => {
    const resolverIp = data.ip;
    const domain = window.location.hostname;

    // Создаём и отправляем на сервер
    const formData = new URLSearchParams();
    formData.append("resolver_ip", resolverIp);
    formData.append("domain", domain);

    return fetch("/add_dns_log", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded"
      },
      body: formData
    });
  })
  .then(() => {
    console.log("IP отправлен.");
  })
  .catch(e => {
    console.error("Ошибка:", e);
  });
