import { fetchUtils, DataProvider } from "react-admin";
import api from "./axios";

const dataProvider: DataProvider = {
  getList: async (resource, params) => {
    const { data } = await api.get(`/${resource}/`, {
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
    if (data.user_id) {
      data.id = data.user_id;
    }
    return { data };
  },

  getMany: async (resource, params) => {
  const { data } = await api.get(`/${resource}/`, {
    params: {
      filter: JSON.stringify({ id: params.ids }),
    },
  });
  return { data };
  },

  create: async (resource, params) => {
    const { data } = await api.post(`/${resource}/`, params.data);
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

  getManyReference: async (resource, params) => {
  const { target, id } = params;

  const { data } = await api.get(`/${resource}/`, {
    params: {
      filter: JSON.stringify({ [target]: id }),
      sort: JSON.stringify(params.sort),
      range: JSON.stringify([
        (params.pagination.page - 1) * params.pagination.perPage,
        params.pagination.page * params.pagination.perPage - 1,
      ]),
    },
  });

  return {
    data,
    total: data.length, // если бэк не возвращает total
    };
  },


} as DataProvider;

export default dataProvider;
