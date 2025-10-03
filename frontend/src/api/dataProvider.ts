import { fetchUtils, DataProvider } from "react-admin";
import api from "./axios";

const dataProvider: DataProvider = {
  getList: async (resource, params) => {
    const { data } = await api.get(`/${resource}`, {
      params: {
        // react-admin присылает pagination + sort
        sort: JSON.stringify(params.sort),
        range: JSON.stringify([
          (params.pagination.page - 1) * params.pagination.perPage,
          params.pagination.page * params.pagination.perPage - 1,
        ]),
        filter: JSON.stringify(params.filter),
      },
    });

    // Бэкенд должен возвращать total (или придётся доставать из headers)
    return {
      data,
      total: data.length, // ⚠️ если бэкенд не шлёт total — временно так
    };
  },

  getOne: async (resource, params) => {
    const { data } = await api.get(`/${resource}/${params.id}`);
    return { data };
  },

  create: async (resource, params) => {
    const { data } = await api.post(`/${resource}`, params.data);
    return { data };
  },

  update: async (resource, params) => {
    const { data } = await api.put(`/${resource}/${params.id}`, params.data);
    return { data };
  },

  delete: async (resource, params) => {
    await api.delete(`/${resource}/${params.id}`);
    return { data: params.previousData };
  },

  // если надо — можно дописать getMany, updateMany, deleteMany
} as DataProvider;

export default dataProvider;
