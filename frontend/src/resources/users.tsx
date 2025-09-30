import { List, Datagrid, TextField } from "react-admin";

export const UserList = () => (
  <List>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="email" />
      <TextField source="full_name" />
      <TextField source="role" />
    </Datagrid>
  </List>
);
