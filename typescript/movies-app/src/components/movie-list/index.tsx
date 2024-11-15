import { Box, Grid, Paper } from '@mui/material';
import React from 'react'
import { MovieDataType } from '../../assets/data';
import MovieCard from '../movie-card';

interface MovieListProps {
    recommendList: MovieDataType[];
}

const MovieList = ({ recommendList}: any) => {
  return (
    <Box sx={{ display: 'flex', gap: 2, overflowX: 'scroll' }}>
      {recommendList.map((movie) => (
        <Grid item key={movie.id}>
          <Paper elevation={0} sx={{ backgroundColor: 'transparent' }}>
            <MovieCard movie={movie} />
          </Paper>
        </Grid>
      ))}
    </Box>
  )
}

export default MovieList