// src/resources/comments.tsx
import {
  List,
  Datagrid,
  TextField,
  DateField,
  ReferenceField,
  Edit,
  SimpleForm,
  TextInput,
  ReferenceInput,
  SelectInput,
  Create,
  Show,
  SimpleShowLayout,
} from "react-admin";
import { required } from "ra-core";

// === LIST ===
export const CommentList = () => (
  <List>
    <Datagrid rowClick="show">
      <ReferenceField source="task_id" reference="tasks" label="Task">
        <TextField source="title" />
      </ReferenceField>
      <ReferenceField source="author_id" reference="users" label="Author">
        <TextField source="full_name" />
      </ReferenceField>
      <TextField source="content" />
      <DateField source="created_at" showTime />
    </Datagrid>
  </List>
);

// === SHOW ===
export const CommentShow = () => (
  <Show>
    <SimpleShowLayout>
      <TextField source="id" />
      <ReferenceField source="task_id" reference="tasks" label="Task">
        <TextField source="title" />
      </ReferenceField>
      <ReferenceField source="author_id" reference="users" label="Author">
        <TextField source="full_name" />
      </ReferenceField>
      <TextField source="content" />
      <DateField source="created_at" showTime />
    </SimpleShowLayout>
  </Show>
);

// === CREATE ===
export const CommentCreate = () => (
  <Create>
    <SimpleForm>
      <ReferenceInput source="task_id" reference="tasks" label="Task">
        <SelectInput optionText="title" validate={[required()]} />
      </ReferenceInput>
      {/* <ReferenceInput source="author_id" reference="users" label="Author">
        <SelectInput optionText="full_name" validate={[required()]} />
      </ReferenceInput> */}
      <TextInput source="content" label="Content" multiline fullWidth validate={[required()]} />
    </SimpleForm>
  </Create>
);

// === EDIT ===
export const CommentEdit = () => (
  <Edit>
    <SimpleForm>
      <ReferenceInput source="task_id" reference="tasks" label="Task">
        <SelectInput optionText="title" />
      </ReferenceInput>
      <ReferenceInput source="author_id" reference="users" label="Author">
        <SelectInput optionText="full_name" />
      </ReferenceInput>
      <TextInput source="content" multiline fullWidth />
    </SimpleForm>
  </Edit>
);
