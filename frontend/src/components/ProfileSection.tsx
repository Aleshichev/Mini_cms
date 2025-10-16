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
  const [form, setForm] = useState({ bio: "" });
  const [avatarFile, setAvatarFile] = useState<File | null>(null);
  const [avatarPreview, setAvatarPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const BACKEND_URL = "http://localhost:8000";
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);

  // Получаем профиль
  useEffect(() => {
    if (!identity?.id) return;

    api
      .get(`/profiles/${identity.id}`)
      .then((res) => {
        setProfile(res.data);
        setForm({ bio: res.data.bio || "" });
        setAvatarPreview(res.data.avatar_url || null);
      })
      .catch(() => {
        setProfile(null);
        setForm({ bio: "" });
        setAvatarPreview(null);
      });
  }, [identity]);

  if (identityLoading || !identity) return null;

  const handleBioChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm((prev) => ({ ...prev, bio: e.target.value }));
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setAvatarFile(file);
      setSelectedFileName(file.name);
    }
  };

  const handleSave = async () => {
    if (!identity?.id) return;
    setLoading(true);

    try {
      let avatar_url = avatarPreview;

      // если выбрано новое фото — загружаем
      if (avatarFile) {
        const formData = new FormData();
        formData.append("file", avatarFile);

        const res = await api.post("/upload/avatar/", formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });

        avatar_url = res.data.avatar_url;
      }

      if (profile) {
        const formData = new FormData();
        formData.append("bio", form.bio);
        if (avatarFile) {
          formData.append("avatar_url", avatarFile);
        }

        await api.put(`/profiles/${identity.id}`, formData, {
          headers: { "Content-Type": "multipart/form-data" },
        });
        alert("Профиль обновлён");
      } else {
        await api.post("/profiles/", {
          user_id: identity.id,
          avatar_url,
          bio: form.bio,
        });
        alert("Профиль создан");
      }

      // Перезагрузка
      const { data } = await api.get(`/profiles/${identity.id}`);
      setProfile(data);
      setForm({ bio: data.bio || "" });
      setAvatarPreview(data.avatar_url || null);
      setOpen(false);
    } catch (e) {
      alert("Ошибка при сохранении профиля");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
      <Button variant="contained" color="primary" size="small" onClick={() => setOpen(true)}>
        My Profile
      </Button>

      <Dialog open={open} onClose={() => setOpen(false)} fullWidth maxWidth="sm">
        <DialogTitle>{profile ? "Редактировать профиль" : "Создать профиль"}</DialogTitle>
        <DialogContent>
          {avatarPreview && (
            <Box sx={{ display: "flex", justifyContent: "center", mb: 2 }}>
              <img
                src={
                  avatarPreview?.startsWith("http")
                    ? avatarPreview
                    : `${BACKEND_URL}${avatarPreview}`
                }
                alt="Avatar preview"
                style={{
                  width: 240,
                  height: 240,
                  objectFit: "cover",
                  borderRadius: "8px",
                }}
              />
            </Box>
          )}

          <Button variant="outlined" component="label">
            {avatarFile ? "Выбрать другое фото" : "Загрузить фото"}
            <input type="file" hidden accept="image/*" onChange={handleFileChange} />
          </Button>

          {selectedFileName && (
            <Box sx={{ mt: 1, fontSize: 14, color: "gray" }}>
              📁 Новое фото: <strong>{selectedFileName}</strong>
            </Box>
          )}
          <TextField
            margin="dense"
            name="bio"
            label="Bio"
            multiline
            fullWidth
            value={form.bio}
            onChange={handleBioChange}
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
