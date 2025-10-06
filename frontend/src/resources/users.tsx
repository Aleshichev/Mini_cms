import { 
  List, Datagrid, TextField, EditButton, DeleteButton, usePermissions,
  Edit, SimpleForm, TextInput, Create, SelectInput, BooleanInput, NumberInput 
} from "react-admin";
import { TextField as TextFieldMui} from "@mui/material";
import { required, email, minLength } from "ra-core";
import { Card, CardContent } from "@mui/material";
import { Button, Dialog, DialogContent } from "@mui/material";
import { useRecordContext } from "react-admin";
import { useState } from "react";
import Typography from "@mui/material/Typography";
import DialogTitle from "@mui/material/DialogTitle";
import { useNavigate } from "react-router-dom";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

import { useEffect } from "react";
import {   useNotify} from "react-admin";
import api from "../api/axios"; // твой axios instance
import { Stack } from "@mui/material";
import {  CircularProgress} from "@mui/material";

const roles = [
  { id: "admin", name: "Admin" },
  { id: "manager", name: "Manager" },
  { id: "back_dev", name: "Backend Dev" },
  { id: "front_dev", name: "Frontend Dev" },
  { id: "tester", name: "Tester" },
  { id: "designer", name: "Designer" },
];

const validatePassword = (value: string) => {
  if (!value) return "Password is required";
  if (value.length < 6) return "Password must be at least 6 characters";
  if (!/[0-9]/.test(value)) return "Password must contain a number";
  if (!/[A-Z]/.test(value)) return "Password must contain an uppercase letter";
  return undefined;
};

const validatePasswordUpdate = (value: string) => {
  if (!value || value.trim() === "") {
    return undefined; // empty field
  }
  if (value.length < 6) return "Password must be at least 6 characters";
  if (!/[0-9]/.test(value)) return "Password must contain a number";
  if (!/[A-Z]/.test(value)) return "Password must contain an uppercase letter";
  return undefined;
};

export const ProfileButton = () => {
  const record = useRecordContext(); // <-- достаём текущую запись (строку из Datagrid)
  const navigate = useNavigate();

  if (!record) return null; // защита от отсутствия данных

  const handleClick = (e: React.MouseEvent) => {
    e.stopPropagation(); // чтобы не триггерился rowClick при клике
    navigate(`/profiles/${record.id}`); // переходим на страницу профиля
  };

  return (
    <Button
      onClick={handleClick}
      size="small"
      startIcon={<AccountCircleIcon />}
    >
      Профиль
    </Button>
  );
};

const MoreInfoButton = () => {
  const record = useRecordContext();
  const [open, setOpen] = useState(false);

  if (!record) return null;

  const handleOpen = (e: React.MouseEvent) => {
    e.stopPropagation(); // <- важно — предотвратить rowClick
    setOpen(true);
  };

  const handleClose = (_event?: {}, _reason?: "backdropClick" | "escapeKeyDown") => {
    setOpen(false);
  };

  return (
    <>
      <Button size="small" onClick={handleOpen}>
        Подробнее
      </Button>

      <Dialog
        open={open}
        onClose={handleClose}
        // предотвращаем случайное всплытие внутри диалога
        onClick={(e) => e.stopPropagation()}
      >
        <DialogTitle>Information about user</DialogTitle>
        <DialogContent dividers>
          <Typography><b>Email:</b> {record.email}</Typography>
          <Typography><b>Projects:</b> {record.projects}</Typography>
          <Typography><b>Tasks:</b> {record.tasks}</Typography>
          <Typography><b>Comments:</b> {record.comments}</Typography>
          {/* добавить что нужно */}
        </DialogContent>
      </Dialog>
    </>
  );
};


export const ProfileSection = () => {
  const record = useRecordContext(); // текущий пользователь из формы
  const [profile, setProfile] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const notify = useNotify();

  useEffect(() => {
    if (!record?.id) return;
    setLoading(true);

    const fetchProfile = async () => {
      try {
        const { data } = await api.get(`/profiles/${record.id}`);
        setProfile(data);
      } catch (err: any) {
        if (err.response?.status === 404) {
          setProfile(null); // профиля нет
        } else {
          notify("Ошибка при загрузке профиля", { type: "error" });
        }
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, [record, notify]);

  const handleSave = async () => {
    if (!record?.id || !profile) return;
    setSaving(true);
    try {
      await api.patch(`/profiles/${record.id}`, {
        avatar_url: profile.avatar_url,
        bio: profile.bio,
      });
      notify("Профиль обновлён", { type: "success" });
    } catch {
      notify("Ошибка при обновлении профиля", { type: "error" });
    } finally {
      setSaving(false);
    }
  };

  const handleCreate = async () => {
    if (!record?.id) return;
    setSaving(true);
    try {
      const { data } = await api.post(`/profiles/`, {
        user_id: record.id,
        avatar_url: profile?.avatar_url || "",
        bio: profile?.bio || "",
      });
      setProfile(data);
      notify("Профиль создан", { type: "success" });
    } catch {
      notify("Ошибка при создании профиля", { type: "error" });
    } finally {
      setSaving(false);
    }
  };

  if (loading)
    return (
      <Card sx={{ mt: 2, p: 2, textAlign: "center" }}>
        <CircularProgress />
      </Card>
    );

  return (
    <Card sx={{ mt: 2, p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Профиль пользователя
      </Typography>

      {profile ? (
        <Stack spacing={2}>
          <TextFieldMui
            label="Avatar URL"
            value={profile.avatar_url || ""}
            onChange={(e) =>
              setProfile({ ...profile, avatar_url: e.target.value })
            }
            fullWidth
          />
          <TextFieldMui
            label="Bio"
            value={profile.bio || ""}
            onChange={(e) => setProfile({ ...profile, bio: e.target.value })}
            fullWidth
            multiline
            minRows={3}
          />
          <Button
            variant="contained"
            onClick={handleSave}
            disabled={saving}
          >
            {saving ? "Сохраняем..." : "Сохранить профиль"}
          </Button>
        </Stack>
      ) : (
        <Button
          variant="outlined"
          onClick={handleCreate}
          disabled={saving}
        >
          {saving ? "Создаём..." : "Создать профиль"}
        </Button>
      )}
    </Card>
  );
};



export const UserList = () => (
  <List>
    <Datagrid rowClick="edit" >
      <TextField source="id" />
      <TextField source="email" />
      <TextField source="full_name" />
      <TextField source="role" />
      <TextField source="is_active" />
      <TextField source="telegram_id" />
      <MoreInfoButton />
      <EditButton />
      {/* <ProfileButton /> */}
      <DeleteButton />
    </Datagrid>
  </List>
);

export const UserEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput source="full_name" validate={[required()]} />
      <TextInput source="email" validate={[required(), email()]} />
      <SelectInput source="role" label="Role" choices={roles} />
      <BooleanInput source="is_active" />
      <NumberInput
        source="telegram_id"
        label="Telegram ID (optional)"
        parse={(value) => (value === "" ? null : Number(value))}
        format={(value) => (value == null ? "" : value)}
      />
      <TextInput source="password" type="password" label="Password" />
      {/* вставляем профиль ниже */}
      <ProfileSection />
    </SimpleForm>
  </Edit>
);
// export const UserEdit = () => (
//   <Edit>
//     <SimpleForm>
//       <TextInput source="full_name" validate={[required()]} />
//       <TextInput source="email" validate={[required(),email()]}/>
//       <SelectInput source="role" label="Role" choices={roles} />
//       <BooleanInput source="is_active" />
//       <NumberInput
//         source="telegram_id"
//         label="Telegram ID (optional)"
//         parse={(value) => (value === "" ? null : Number(value))}
//         format={(value) => (value == null ? "" : value)}
//       />
//       <TextInput source="password" type="password" label="Password"/>
//     </SimpleForm>
//   </Edit>
// );

export const UserCreate = () => (
  <Create>
    <SimpleForm defaultValues={{ is_active: true }}>
      <TextInput source="full_name" validate={[required()]} />
      <TextInput source="email" validate={[required(), email()]}/>
      <SelectInput source="role" label="Role" choices={roles}  validate={[required()]} />
      <NumberInput
        source="telegram_id"
        label="Telegram ID (optional)"
        parse={(value) => (value === "" ? null : Number(value))}
        format={(value) => (value == null ? "" : value)}
      />
      <TextInput
        source="password"
        type="password"
        label="Password"
        validate={validatePassword} />
    </SimpleForm>
  </Create>
);
