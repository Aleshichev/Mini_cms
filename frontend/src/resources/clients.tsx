// src/resources/clients.tsx

import {
  List,
  Datagrid,
  TextField,
  EmailField,
  DateField,
  Edit,
  SimpleForm,
  TextInput,
  NumberInput,
  required,
  email,
  Create,
  EditButton,
  DeleteButton,
  useRecordContext,
  useGetOne,
} from "react-admin";
import {
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  Typography,
  CircularProgress,
} from "@mui/material";
import { useState } from "react";

// src/utils/validators.ts

export const validatePhone = (value: string) => {
  if (!value) return undefined; // разрешаем пустое поле
  if (value.length > 13) {
    return "Phone number must not be longer than 13 characters";
  }
  const regex = /^\+\d{12}$/;
  if (!regex.test(value)) {
    return "Phone must start with '+' and contain exactly 12 digits";
  }
  return undefined; // всё ок
};

export const DealsInfoButton = () => {
  const record = useRecordContext();
  const [open, setOpen] = useState(false);

  if (!record) return null;

  const handleOpen = (e: React.MouseEvent) => {
    e.stopPropagation();
    setOpen(true);
  };

  const handleClose = () => setOpen(false);

  const { data, isLoading } = useGetOne("clients", { id: record.id }, { enabled: open });
  if (!record.deals || record.deals.length === 0) {
    return null;
  }

  return (
    <>
      <Button size="small" onClick={handleOpen}>
        Deals Info
      </Button>

      <Dialog open={open} onClose={handleClose} onClick={(e) => e.stopPropagation()}>
        <DialogTitle>Deals for {data?.full_name}</DialogTitle>
        <DialogContent dividers>
          {isLoading && <CircularProgress />}
          {data?.deals && data.deals.length > 0 ? (
            data.deals.map((deal: any) => (
              <div key={deal.id} style={{ marginBottom: "12px", paddingLeft: "16px" }}>
                <Typography variant="body1">
                  • <b>{deal.title}</b>
                </Typography>
                {deal.status && (
                  <Typography
                    variant="body1"
                    sx={{
                      color:
                        deal.status === "new"
                          ? "green"
                          : deal.status === "in_progress"
                          ? "orange"
                          : deal.status === "completed"
                          ? "gray"
                          : "text.secondary",
                      fontStyle: "italic",
                      marginLeft: "10px",
                    }}
                  >
                    {deal.status === "new"
                      ? "New Deal"
                      : deal.status === "in_progress"
                      ? "In Progress"
                      : deal.status === "completed"
                      ? "Completed"
                      : deal.status}
                  </Typography>
                )}
              </div>
            ))
          ) : (
            <Typography>No deals found</Typography>
          )}
        </DialogContent>
      </Dialog>
    </>
  );
};


// --- Список клиентов
export const ClientList = () => (
  <List>
    <Datagrid rowClick="edit">
      <TextField source="full_name" />
      <EmailField source="email" />
      <TextField source="phone" />
      <TextField source="telegram_id" />
      <DateField source="created_at" />
      <DealsInfoButton />
      <EditButton />
      <DeleteButton />
    </Datagrid>
  </List>
);


// --- Форма редактирования
export const ClientEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput source="full_name" validate={[required()]}/>
      <TextInput source="email" validate={[required(), email()]}/>
      <TextInput source="phone" validate={[required(), validatePhone]} />
      <NumberInput
        source="telegram_id"
        parse={(value) => (value === "" ? null : Number(value))}
        format={(value) => (value == null ? "" : value)}
      />
    </SimpleForm>
  </Edit>
);


// --- Форма создания
export const ClientCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="full_name" validate={[required()]} />
      <TextInput source="email" validate={[required(), email()]} />
      <TextInput source="phone" validate={[required(), validatePhone]} />
      <NumberInput
        source="telegram_id"
        parse={(value) => (value === "" ? null : Number(value))}
        format={(value) => (value == null ? "" : value)}
      />
    </SimpleForm>
  </Create>
);
