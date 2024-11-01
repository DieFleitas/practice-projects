import { Box, Grid, Paper } from '@mui/material';
import React from 'react';
import { MovieDataType } from '../../assets/data';

interface MovieTrendListProps {
  trendingList: MovieDataType[];
}

const MovieTrendList = ({ trendingList }: MovieTrendListProps) => {
  return (
    <Box sx={{ display: 'flex', gap: 2, overflowX: 'scroll' }}>
      {trendingList.map((movie) => (
        <Grid item key={movie.id}>
          <Paper elevation={0} sx={{ backgroundColor: 'transparent' }}>
            <MovieTrendCard movie={movie} />
          </Paper>
        </Grid>
      ))}
    </Box>
  );
};

export default MovieTrendList;
