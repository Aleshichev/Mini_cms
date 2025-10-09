import { 
  List, Datagrid, TextField, EditButton, DeleteButton, usePermissions,
  Edit, SimpleForm, TextInput, Create, SelectInput, BooleanInput, NumberInput 
} from "react-admin";
import { required, email, minLength } from "ra-core";
import { Button, Dialog, DialogContent } from "@mui/material";
import { useRecordContext, useGetOne } from "react-admin";
import { useState } from "react";
import Typography from "@mui/material/Typography";
import DialogTitle from "@mui/material/DialogTitle";
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

const MoreInfoButton = () => {
  const record = useRecordContext();
  const [open, setOpen] = useState(false);

  if (!record) return null;

  const handleOpen = (e: React.MouseEvent) => {
    e.stopPropagation();
    setOpen(true);
  };

  const handleClose = () => setOpen(false);

  // Выполняем запрос к API /users/:id только если диалог открыт
  const { data, isLoading } = useGetOne("users", { id: record.id }, { enabled: open });
  
  return (
    <>
      <Button size="small" onClick={handleOpen}>
        More Info
      </Button>

      <Dialog open={open} onClose={handleClose} onClick={(e) => e.stopPropagation()}>
        <DialogTitle>Info about {data?.full_name}</DialogTitle>
        <DialogContent dividers>
          {isLoading && <CircularProgress />}
          {data && (
            <>
              <Typography><b>Name:</b> {data.full_name}</Typography>
              <Typography><b>Email:</b> {data.email}</Typography>
              <Typography><b>Role:</b> {data.role}</Typography>
              
              <Typography sx={{ mt: 2 }}><b>Deals:</b></Typography>
             {data.deals?.length ? (
               data.deals.map((t: any) => (
                 <Typography key={t.id} sx={{ pl: 2 }}>• {t.title}</Typography>
               ))
             ) : (
               <Typography sx={{ pl: 2 }}>No deals</Typography>
             )}

              <Typography sx={{ mt: 2 }}><b>Projects:</b></Typography>
              {data.projects?.length ? (
                data.projects.map((p: any) => (
                  <Typography key={p.id} sx={{ pl: 2 }}>• {p.name}</Typography>
                ))
              ) : (
                <Typography sx={{ pl: 2 }}>No projects</Typography>
              )}

              <Typography sx={{ mt: 2 }}><b>Tasks:</b></Typography>
              {data.tasks?.length ? (
                data.tasks.map((t: any) => (
                  <Typography key={t.id} sx={{ pl: 2 }}>• {t.title}</Typography>
                ))
              ) : (
                <Typography sx={{ pl: 2 }}>No tasks</Typography>
              )}
            </>
          )}
        </DialogContent>
      </Dialog>
    </>
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
    </SimpleForm>
  </Edit>
);


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
