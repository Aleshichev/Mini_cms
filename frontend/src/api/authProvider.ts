import { AuthProvider } from "react-admin";
import api from "./axios";

export const authProvider: AuthProvider = {
  login: async ({ username, password }) => {
    try {
      const formData = new FormData();
      formData.append("email", username); // поле должно совпадать с Form() на бэке
      formData.append("password", password);

      const { data } = await api.post("/auth/login/", formData);

      localStorage.setItem("access_token", data.access_token);
      localStorage.setItem("refresh_token", data.refresh_token);

      return Promise.resolve();
    } catch (error: any) {
      return Promise.reject(error.response?.data?.detail || "Login failed");
    }
  },

  logout: async () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    return Promise.resolve();
  },

  checkAuth: async () => {
    const token = localStorage.getItem("access_token");
    if (!token) return Promise.reject();

    try {
      const { data } = await api.get("/auth/user/me/");
      localStorage.setItem("user", JSON.stringify(data));
      return Promise.resolve();
    } catch {
      const refresh = localStorage.getItem("refresh_token");
      if (!refresh) return Promise.reject();

      try {
        const { data } = await api.post("/auth/refresh/", { refresh_token: refresh });
        localStorage.setItem("access_token", data.access_token);
        return Promise.resolve();
      } catch {
        return Promise.reject();
      }
    }
  },

  checkError: (error) => {
    if (error.status === 401 || error.status === 403) return Promise.reject();
    return Promise.resolve();
  },

  getIdentity: async () => {
    const { data } = await api.get("/auth/user/me/");
    return {
      id: data.id,
      fullName: data.full_name,
      role: data.role,
    };
  },

  getPermissions: async () => {
    const { data } = await api.get("/auth/user/me/");
    return Promise.resolve(data.role);
  },
};
