import {
  List,
  Datagrid,
  TextField,
  DateField,
  Show,
  SimpleShowLayout,
  NumberInput,
  ReferenceInput,
  SelectInput,
  EditButton,
  DeleteButton,
  ArrayField,
  Edit,
  Create,
  SimpleForm,
  TextInput,
  required,
  NumberField,
} from "react-admin";

export const ProjectList = () => (
  <List>
    <Datagrid rowClick="show">
      <NumberField source="number" />
      <TextField source="type" />
      <TextField source="description" />
      <EditButton />
      <DeleteButton />
    </Datagrid>
  </List>
);
export const ProjectShow = () => (
  <Show>
    <SimpleShowLayout>
      <TextField source="number" />
      <TextField source="type" />
      <TextField source="description" />
      <DateField source="created_at" />

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
       <TextInput source="description" multiline fullWidth />
      </SimpleForm>
    </Edit>
  );

  export const ProjectCreate = () => (
    <Create>
      <SimpleForm>
        <NumberInput source="number" validate={[required()]} />
        <ReferenceInput source="project_id" reference="projects">
          <SelectInput optionText="type" validate={[required()]} />
        </ReferenceInput> 
        <TextInput source="description" multiline fullWidth />
      </SimpleForm>
    </Create>
  );