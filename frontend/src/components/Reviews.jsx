import React, { useState, useEffect } from "react";
import axios from "../utils/axios-config";
import { getAuthHeader } from "../utils/user";
import { Card, CardContent, Typography, Rating, Grid, Box } from "@mui/material";

export function Reviews() {
  const [statsRawData, setStatsRawData] = useState([]);
  const dtmFormattingOptions = { year: "numeric", month: "long", day: "numeric" };

  useEffect(() => {
    const queryData = async () => {
      const response = await axios.get("/reviews/", { headers: getAuthHeader() });
      setStatsRawData(response.data);
    };
    queryData();
  }, []);

  const card = statsRawData.map((data) => {
    const dtmCreated = new Date(data.created_dtm);

    let dateString = dtmCreated.toLocaleDateString("ru-ru", dtmFormattingOptions);
    if (data.edited_dtm) {
      const dtmEdited = new Date(data.edited_dtm);
      const editedSting = dtmEdited.toLocaleDateString("ru-ru", dtmFormattingOptions);
      dateString += ` (ред. ${editedSting})`;
    }
    return (
      <React.Fragment>
        <CardContent align="left">
          <Typography variant="h6" component="div">
            {data.user_name}
          </Typography>
          <Typography variant="p" component="div">
            {dateString}
          </Typography>
          <Rating name="read-only" value={data.rating} readOnly />
          <Typography sx={{ mb: 1.5 }} color="text.secondary">
            {data.gis_org.org_name}
          </Typography>
          <Typography variant="body2">{data.text}</Typography>
        </CardContent>
      </React.Fragment>
    );
  });

  return (
    <Grid align="center" sx={{ mb: "1rem" }}>
      <Box style={{ width: 800 }} sx={{ mt: "1rem" }}>
        <Typography variant="h5" sx={{ mb: "1rem" }}>
          Отзывы
        </Typography>
        <Card variant="outlined">{card}</Card>
      </Box>
    </Grid>
  );
}

export default Reviews;
