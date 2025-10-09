// src/admin/deals/DealResource.tsx

import {
  List,
  Datagrid,
  TextField,
  ReferenceField,
  DateField,
  Edit,
  Create,
  SimpleForm,
  TextInput,
  ReferenceInput,
  SelectInput,
  required,
  EditButton,
  DeleteButton,
} from "react-admin";

// Статусы сделки (enum DealStatus)
const statusChoices = [
  { id: "new", name: "New" },
  { id: "in_progress", name: "In Progress" },
  { id: "completed", name: "Completed" },
];

// ✅ Список сделок
export const DealList = () => (
  <List>
    <Datagrid rowClick="edit">
      <TextField source="title" />
      <TextField source="status" />
      <ReferenceField source="client_id" reference="clients" label="Client" link={false}>
        <TextField source="full_name" />
      </ReferenceField>
      <ReferenceField source="manager_id" reference="users" label="Manager" link={false}>
        <TextField source="email" />
      </ReferenceField>
      <ReferenceField source="project_id" reference="projects" label="Project">
        <TextField source="name" />
      </ReferenceField>
      <DateField source="created_at" />
      <EditButton />
      <DeleteButton />
    </Datagrid>
  </List>
);

// ✅ Редактирование сделки
export const DealEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput source="title" validate={[required()]} />
      <TextInput source="description" multiline fullWidth />
      <SelectInput source="status" choices={statusChoices} validate={[required()]} />

      <ReferenceInput source="client_id" reference="clients">
        <SelectInput optionText="full_name" validate={[required()]} />
      </ReferenceInput>

      <ReferenceInput source="manager_id" reference="users">
        <SelectInput optionText="email" validate={[required()]} />
      </ReferenceInput>

      <ReferenceInput source="project_id" reference="projects">
        <SelectInput optionText="name" validate={[required()]} />
      </ReferenceInput>
    </SimpleForm>
  </Edit>
);

// ✅ Создание сделки
export const DealCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="title" validate={[required()]} />
      <TextInput source="description" multiline fullWidth />
      <SelectInput source="status" choices={statusChoices} defaultValue="new" validate={[required()]} />

      <ReferenceInput source="client_id" reference="clients">
        <SelectInput optionText="full_name" validate={[required()]} />
      </ReferenceInput>

      <ReferenceInput source="manager_id" reference="users">
        <SelectInput optionText="email" validate={[required()]} />
      </ReferenceInput>

      <ReferenceInput source="project_id" reference="projects">
        <SelectInput optionText="name" validate={[required()]} />
      </ReferenceInput>
    </SimpleForm>
  </Create>
);
