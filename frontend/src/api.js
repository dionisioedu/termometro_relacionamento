import axios from "axios";
import Cookies from "js-cookie";

const api = axios.create({
    baseURL: "https://backend-n2ol.onrender.com",
    withCredentials: true,  // Necessário para enviar cookies
});

api.interceptors.request.use(config => {
    const csrftoken = Cookies.get("csrftoken");
    if (csrftoken) {
        config.headers["X-CSRFToken"] = csrftoken;
    }
    return config;
});

export default api;
