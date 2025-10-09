// src/admin/projects/ProjectResource.tsx

import {
  List,
  Datagrid,
  TextField,
  DateField,
  Show,
  SimpleShowLayout,
  ShowButton,
  EditButton,
  DeleteButton,
  ArrayField,
  Edit,
  Create,
  SimpleForm,
  TextInput,
  required,
} from "react-admin";

// ✅ Список проектов
export const ProjectList = () => (
  <List>
    <Datagrid rowClick="show">
      <TextField source="name" />
      <TextField source="description" />
      <EditButton />
      <DeleteButton />
    </Datagrid>
  </List>
);
export const ProjectShow = () => (
  <Show>
    <SimpleShowLayout>
      <TextField source="name" />
      <TextField source="description" />
      <DateField source="created_at" />

      {/* 👥 Пользователи проекта */}
      <ArrayField source="users" label="Users in Project">
        <Datagrid>
          <TextField source="full_name" />
          <TextField source="email" />
        </Datagrid>
      </ArrayField>


        <ArrayField source="tasks" label="Tasks in Project">
        <Datagrid>
          <TextField source="id" />
          <TextField source="title" />
          <TextField source="status" />
          <DateField source="due_date" />
        </Datagrid>
              </ArrayField>
    </SimpleShowLayout>
  </Show>
);
  export const ProjectEdit = () => (
    <Edit>
      <SimpleForm>
        <TextInput source="name" validate={[required()]} />
        <TextInput source="description" multiline fullWidth />
      </SimpleForm>
    </Edit>
  );

  // ✅ Создание проекта
  export const ProjectCreate = () => (
    <Create>
      <SimpleForm>
        <TextInput source="name" validate={[required()]} />
        <TextInput source="description" multiline fullWidth />
      </SimpleForm>
    </Create>
  );