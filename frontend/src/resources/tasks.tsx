import {
  List,
  Datagrid,
  TextField,
  EditButton,
  DeleteButton,
  useGetOne,
  useRecordContext,
  DateField,
  Edit,
  SimpleForm,
  TextInput,
  DateInput,
  BooleanInput,
  ReferenceInput,
  SelectInput,
  Create,
  required,
} from "react-admin";
import { useState } from "react";
import {
  Button,
  Dialog,
  DialogContent,
  DialogTitle,
  CircularProgress,
  Typography,
} from "@mui/material";

const MoreInfoButton = () => {
  const record = useRecordContext();
  const [open, setOpen] = useState(false);

  if (!record) return null;

  const handleOpen = (e: React.MouseEvent) => {
    e.stopPropagation();
    setOpen(true);
  };

  const handleClose = () => setOpen(false);

  const { data, isLoading } = useGetOne("tasks", { id: record.id }, { enabled: open });

  return (
    <>
      <Button size="small" onClick={handleOpen}>
        More Info
      </Button>

      <Dialog
        open={open}
        onClose={handleClose}
        onClick={(e) => e.stopPropagation()}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>Info about task "{data?.title}"</DialogTitle>
        <DialogContent dividers>
          {isLoading && <CircularProgress />}
          {data && (
            <>
              <DateField source="due_date" showTime />

              <Typography sx={{ mt: 1 }}>
                <b>Completed:</b> {data.completed ? "✅ Yes" : "❌ No"}
              </Typography>

              <Typography sx={{ mt: 1 }}>
                <b>Manager:</b> {data.manager?.full_name || "No manager"}
              </Typography>

              <Typography sx={{ mt: 2 }}>
                <b>Comments:</b>
              </Typography>
              {data.comments?.length ? (
                data.comments.map((c: any) => (
                  <Typography key={c.id} sx={{ pl: 2, mt: 0.5 }}>
                    • {c.content}
                  </Typography>
                ))
              ) : (
                <Typography sx={{ pl: 2 }}>No comments</Typography>
              )}
            </>
          )}
        </DialogContent>
      </Dialog>
    </>
  );
};

export const TaskList = () => (
  <List>
    <Datagrid rowClick="edit">
      <TextField source="title" />
      <TextField source="description" />
      <DateField source="due_date" showTime />
      <TextField source="completed" />
      <MoreInfoButton />
      <EditButton />
      <DeleteButton />
    </Datagrid>
  </List>
);

export const TaskEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput source="title" validate={[required()]} fullWidth />
      <TextInput source="description" multiline fullWidth />
      <DateInput source="due_date" />
      <BooleanInput source="completed" />
      <ReferenceInput source="manager_id" reference="users" label="Manager">
        <SelectInput optionText="full_name" />
      </ReferenceInput>
      <ReferenceInput source="project_id" reference="projects" label="Project">
        <SelectInput optionText="number" />
      </ReferenceInput>
    </SimpleForm>
  </Edit>
);

export const TaskCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="title" validate={[required()]} fullWidth />
      <TextInput source="description" multiline fullWidth />
      <DateInput source="due_date" />
      <BooleanInput source="completed" />

      <ReferenceInput source="manager_id" reference="users" label="Manager">
        <SelectInput optionText="full_name" />
      </ReferenceInput>

      <ReferenceInput source="project_id" reference="projects" label="Project">
        <SelectInput optionText="number" />
      </ReferenceInput>
    </SimpleForm>
  </Create>
);
