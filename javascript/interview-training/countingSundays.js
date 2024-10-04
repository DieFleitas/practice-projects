const sundays = () => {
  // 1 1900 jan was a monday
  // 365, leap year 366

  let res = 0;
  for (let year = 1091; year <= 2000; year++) {
    for (let month = 0; month < 12; month++) {
      const day = new Date(year, month, 1).getDay();
      if (day === 0) {
        res++;
      }
    }
  }
};
