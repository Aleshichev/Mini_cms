import { AppBar, TitlePortal, useGetIdentity } from "react-admin";
import { Typography, Box } from "@mui/material";
import { ProfileSection } from "./ProfileSection";

export const MyAppBar = (props: any) => {
  const { data: identity } = useGetIdentity();

  return (
    <AppBar
      {...props}
      color="secondary"
      elevation={1}
      sx={{
        "& .RaAppBar-title": { flex: 1 },
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        pr: 2,
      }}
    >
      <TitlePortal />
      <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
        {identity && (
          <Typography variant="body2">👤 {identity.full_name || identity.email}</Typography>
        )}
        <ProfileSection />
      </Box>
    </AppBar>
  );
};
