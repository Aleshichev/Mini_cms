import {
  List,
  Datagrid,
  TextField,
  EditButton,
  DeleteButton,
  useGetOne,
  useRecordContext,
} from "react-admin";
import { useState } from "react";
import { Button, Dialog, DialogContent, DialogTitle, CircularProgress, Typography } from "@mui/material";

const MoreInfoButton = () => {
  const record = useRecordContext();
  const [open, setOpen] = useState(false);

  if (!record) return null;

  const handleOpen = (e: React.MouseEvent) => {
    e.stopPropagation();
    setOpen(true);
  };

  const handleClose = () => setOpen(false);

  // Запрос задачи с деталями (например: project, manager, comments)
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
              <Typography>
                <b>Due date:</b>{" "}
                {data.due_date
                  ? new Date(data.due_date).toLocaleString()
                  : "No due date"}
              </Typography>

              <Typography sx={{ mt: 1 }}>
                <b>Completed:</b> {data.completed ? "✅ Yes" : "❌ No"}
              </Typography>

              <Typography sx={{ mt: 2 }}>
                <b>Project:</b> {data.project?.number || "No project"} <br />
                <b>Type:</b> {data.project?.type || "No project"}
              </Typography>

              <Typography sx={{ mt: 1 }}>
                <b>Manager:</b> {data.manager?.full_name || "No manager"}
              </Typography>

              <Typography sx={{ mt: 2 }}><b>Comments:</b></Typography>
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
      <TextField source="due_date" />
      <TextField source="completed" />
      <MoreInfoButton />
      <EditButton />
      <DeleteButton />
    </Datagrid>
  </List>
);
