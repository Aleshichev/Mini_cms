import { Admin, Resource } from "react-admin";
import { authProvider } from "./api/authProvider";
import { Dashboard } from "./pages/Dashboard";
import { UserList } from "./resources/users";
// import { ClientList } from "./resources/clients";
// import { DealList } from "./resources/deals";
// import { TaskList } from "./resources/tasks";
// import { ProjectList } from "./resources/projects";
// import { ProfileList } from "./resources/profiles";
// import { CommentList } from "./resources/comments";
import dataProvider from "./api/dataProvider";

function App() {
  return (
    <Admin
      dashboard={Dashboard}
      authProvider={authProvider}
      dataProvider={dataProvider}
    >
      <Resource name="user" list={UserList} />
      {/* <Resource name="clients" list={ClientList} />
      <Resource name="deals" list={DealList} />
      <Resource name="tasks" list={TaskList} />
      <Resource name="projects" list={ProjectList} />
      <Resource name="profiles" list={ProfileList} />
      <Resource name="comments" list={CommentList} /> */}
    </Admin>
  );
}

export default App;
