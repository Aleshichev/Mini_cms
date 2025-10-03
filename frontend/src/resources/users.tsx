// import { List, Datagrid, TextField } from "react-admin";

// export const UserList = () => (
//   <List>
//     <Datagrid rowClick="edit">
//       <TextField source="id" />
//       <TextField source="email" />
//       <TextField source="full_name" />
//       <TextField source="role" />
//     </Datagrid>
//   </List>
// );
// --------------------------------------------------------------
// import { List, Datagrid, TextField, EditButton, DeleteButton, Edit, SimpleForm, TextInput, Create } from "react-admin";

// export default {
//   list: () => (
//     <List>
//       <Datagrid rowClick="edit">
//         <TextField source="id" />
//         <TextField source="email" />
//         <TextField source="full_name" />
//         <TextField source="role" />
//         <EditButton />
//         <DeleteButton />
//       </Datagrid>
//     </List>
//   ),
//   edit: () => (
//     <Edit>
//       <SimpleForm>
//         <TextInput source="email" />
//         <TextField source="full_name" />
//       </SimpleForm>
//     </Edit>
//   ),
//   create: () => (
//     <Create>
//       <SimpleForm>
//         <TextInput source="email" />
//         <TextField source="username" />
//       </SimpleForm>
//     </Create>
//   )
// };
// --------------------------------------------------------------
import { 
  List, Datagrid, TextField, EditButton, DeleteButton, 
  Edit, SimpleForm, TextInput, Create, SelectInput, BooleanInput, NumberInput 
} from "react-admin";
import { required, email, minLength } from "ra-core";

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

export const UserList = () => (
  <List>
    <Datagrid rowClick="edit">
      <TextField source="id" />
      <TextField source="email" />
      <TextField source="full_name" />
      <TextField source="role" />
      <TextField source="is_active" />
      <TextField source="telegram_id" />
      <EditButton />
      <DeleteButton />
    </Datagrid>
  </List>
);

export const UserEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput source="full_name" validate={[required()]}/>
      <TextInput source="email" validate={[required(), email()]}/>
      <SelectInput source="role" label="Role" choices={roles} validate={[required()]} />
      <BooleanInput source="is_active" />
      <NumberInput
        source="telegram_id"
        label="Telegram ID (optional)"
        parse={(value) => (value === "" ? null : Number(value))}
        format={(value) => (value == null ? "" : value)}
      />
      <TextInput source="password" type="password" label="Password" validate={validatePassword} />
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
