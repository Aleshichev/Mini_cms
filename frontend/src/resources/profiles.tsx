import { Edit, SimpleForm, TextInput, Create } from "react-admin";

// ===================== PROFILES =====================

export const ProfileEdit = () => (
  <Edit>
    <SimpleForm>
      <TextInput source="avatar_url" label="Avatar URL" />
      <TextInput source="bio" label="Bio" multiline />
    </SimpleForm>
  </Edit>
);

export const ProfileCreate = () => (
  <Create>
    <SimpleForm>
      <TextInput source="avatar_url" label="Avatar URL" />
      <TextInput source="bio" label="Bio" multiline/>
    </SimpleForm>
  </Create>
);
