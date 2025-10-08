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
import api from "../api/axios";

export const ProfileSection = () => {
  const { data: identity, isLoading: identityLoading } = useGetIdentity();
  const [profile, setProfile] = useState<any>(null);
  const [open, setOpen] = useState(false);
  const [form, setForm] = useState({ avatar_url: "", bio: "" });
  const [loading, setLoading] = useState(false);

  // Загружаем профиль по ID пользователя
 useEffect(() => {
  console.log("identity.id", identity?.id); // 👈
  if (!identity?.id) return;

  api
    .get(`/profiles/${identity.id}`)
    .then((res) => {
      console.log("Profile loaded:", res.data); // 👈
      setProfile(res.data);
      setForm({
        avatar_url: res.data.avatar_url || "",
        bio: res.data.bio || "",
      });
    })
    .catch((err) => {
      console.warn("❌ Profile not found", err); // 👈
      setProfile(null);
      setForm({ avatar_url: "", bio: "" });
    });
}, [identity]);


  // пока грузится identity — ничего не рендерим
  if (identityLoading || !identity) return null;

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSave = async () => {
    if (!identity?.id) return;
    setLoading(true);
    try {
      if (profile) {
        // 🔄 Профиль уже есть — обновляем
        await api.put(`/profiles/${identity.id}`, {
          avatar_url: form.avatar_url,
          bio: form.bio,
        });
        alert("Профиль обновлён");
      } else {
        // ➕ Профиля нет — создаём
        await api.post("/profiles/", {
          user_id: identity.id,
          avatar_url: form.avatar_url,
          bio: form.bio,
        });
        alert("Профиль создан");
      }

      // Перезагружаем профиль
      const { data } = await api.get(`/profiles/${identity.id}`);
      setProfile(data);
      setForm({
        avatar_url: data.avatar_url || "",
        bio: data.bio || "",
      });
      setOpen(false);
    } catch (e) {
      alert("Ошибка при сохранении профиля");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
      <Button
        variant="contained"
        color="primary"
        size="small"
        onClick={() => setOpen(true)}
      >
        My Profile
      </Button>

      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm">
        <DialogTitle>
          {profile ? "Редактировать профиль" : "Создать профиль"}
        </DialogTitle>
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
          <Button onClick={handleSave} disabled={loading}>
            {loading ? <CircularProgress size={20} /> : profile ? "Сохранить" : "Создать"}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
