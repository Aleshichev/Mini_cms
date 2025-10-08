import { useState, useEffect } from "react";
import { useGetIdentity } from "react-admin";
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  CircularProgress,
  Box,
} from "@mui/material";
import api from "../api/axios"; // проверь путь к axios

export const ProfileSection = () => {
  const { data: identity, isLoading: identityLoading } = useGetIdentity();
  const [profile, setProfile] = useState<any>(null);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ avatar_url: "", bio: "" });
  const [loading, setLoading] = useState(false);

  // 🔹 Загружаем профиль, только если identity уже есть
  useEffect(() => {
    if (!identity?.id) return;
    api
      .get(`/profiles/${identity.id}`)
      .then((res) => setProfile(res.data))
      .catch(() => setProfile(null)); // если 404 → профиля нет
  }, [identity]);

  // пока грузится — ничего не рендерим
  if (identityLoading || !identity) return null;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };
  

  const handleCreate = async () => {
    if (!identity?.id) {console.warn("❌ Нет identity.id", identity);
        return;}
    setLoading(true);
    try {
      await api.post("/profiles/", {
        user_id: identity.id,
        avatar_url: form.avatar_url,
        bio: form.bio,
      });
      const { data } = await api.get(`/profiles/${identity.id}`);
      setProfile(data);
      alert("Профиль успешно создан!");
      setOpen(false);
    } catch (e) {
      alert("Ошибка при создании профиля (проверь API)");
    } finally {
      setLoading(false);
    }
  };

  const handleEdit = () => {
    if (!identity?.id) return;
    window.location.href = `#/profiles/${identity.id}`; // переход в React-Admin edit
  };

  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
      {profile ? (
        <Button
          variant="outlined"
          color="secondary"
          size="small"
          onClick={handleEdit}
        >
          Редактировать профиль
        </Button>
      ) : (
        <>
          <Button
            variant="contained"
            color="primary"
            size="small"
            onClick={() => setOpen(true)}
          >
            Создать профиль
          </Button>

          <Dialog open={open} onClose={() => setOpen(false)}>
            <DialogTitle>Создать профиль</DialogTitle>
            <DialogContent>
              <TextField
                margin="dense"
                name="avatar_url"
                label="Avatar URL"
                fullWidth
                value={form.avatar_url}
                onChange={handleChange}
              />
              <TextField
                margin="dense"
                name="bio"
                label="Bio"
                multiline
                fullWidth
                value={form.bio}
                onChange={handleChange}
              />
            </DialogContent>
            <DialogActions>
              <Button onClick={() => setOpen(false)}>Отмена</Button>
              <Button onClick={handleCreate} disabled={loading}>
                {loading ? <CircularProgress size={20} /> : "Создать"}
              </Button>
            </DialogActions>
          </Dialog>
        </>
      )}
    </Box>
  );
};
