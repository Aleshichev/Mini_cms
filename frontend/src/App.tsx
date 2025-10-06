import { Admin, Resource } from "react-admin";
import { authProvider } from "./api/authProvider";
import { Dashboard } from "./pages/Dashboard";
import { UserList, UserEdit, UserCreate } from "./resources/users";
import { ProfileEdit, ProfileCreate } from "./resources/profiles";
// import Users from "./resources/users";
// import { ClientList } from "./resources/clients";
// import { DealList } from "./resources/deals";
// import { TaskList } from "./resources/tasks";
// import { ProjectList } from "./resources/projects";
// import { CommentList } from "./resources/comments";
import dataProvider from "./api/dataProvider";
import { MyLayout } from "./components/MyLayout";
function App() {
  return (
    <Admin
      dashboard={Dashboard}
      authProvider={authProvider}
      dataProvider={dataProvider}
       layout={MyLayout}
    >
      <Resource name="users" list={UserList} edit={UserEdit} create={UserCreate} />
      <Resource name="profiles" edit={ProfileEdit} create={ProfileCreate} />
      {/* <Resource name="user" {...Users} /> */}
      {/* <Resource name="clients" list={ClientList} />
      <Resource name="deals" list={DealList} />
      <Resource name="tasks" list={TaskList} />
      <Resource name="projects" list={ProjectList} />
      <Resource name="comments" list={CommentList} /> */}
    </Admin>
  );
}

export default App;
