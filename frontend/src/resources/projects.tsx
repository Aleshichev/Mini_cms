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

const projectTypeChoices = [
  { id: "web_site", name: "Web site" },
  { id: "mobile_app", name: "Mobile app" },
  { id: "desktop_app", name: "Desktop app" },
  { id: "telegram_bot", name: "Telegram bot" },

];


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
      <SelectInput source="type" choices={projectTypeChoices} validate={[required()]} label="Project type"/>
      <TextInput source="description" multiline fullWidth />
    </SimpleForm>
  </Create>
);