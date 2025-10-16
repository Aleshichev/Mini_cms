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

const statusChoices = [
  { id: "new", name: "New" },
  { id: "in_progress", name: "In Progress" },
  { id: "completed", name: "Completed" },
];

const projectTypeChoices = [
  { id: "web_site", name: "Web site" },
  { id: "mobile_app", name: "Mobile app" },
  { id: "desktop_app", name: "Desktop app" },
  { id: "telegram_bot", name: "Telegram bot" },
];

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
      <ReferenceField source="project_id" reference="projects" label="Project" link={false}>
        <TextField source="number" />
      </ReferenceField>
      <DateField source="created_at" />
      <EditButton />
      <DeleteButton />
    </Datagrid>
  </List>
);

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

      <SelectInput
        source="type"
        choices={projectTypeChoices}
        validate={[required()]}
        label="Project type"
      />
    </SimpleForm>
  </Edit>
);

export const DealCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="title" validate={[required()]} />
      <TextInput source="description" multiline fullWidth />
      <SelectInput
        source="status"
        choices={statusChoices}
        defaultValue="new"
        validate={[required()]}
      />

      <ReferenceInput source="client_id" reference="clients">
        <SelectInput optionText="full_name" validate={[required()]} />
      </ReferenceInput>

      <ReferenceInput source="manager_id" reference="users">
        <SelectInput optionText="email" validate={[required()]} />
      </ReferenceInput>

      <ReferenceInput source="project_id" reference="projects">
        <SelectInput optionText="number" validate={[required()]} />
      </ReferenceInput>
      {/* <SelectInput source="type" choices={projectTypeChoices} validate={[required()]} label="Project type"/> */}
    </SimpleForm>
  </Create>
);
