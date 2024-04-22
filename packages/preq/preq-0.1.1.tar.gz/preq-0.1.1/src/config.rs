use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Config {
    python_command: String,
    fallback_data_file: String,
}

impl Config {
    fn new() -> Self {
        let mut settings = config::Config::default();
        settings
            // Start off by merging in the "default" configuration file
            .merge(config::File::with_name("Config"))
            .unwrap()
            // Add in settings from the environment (with a prefix of APP)
            // Eg.. `APP_DEBUG=1 ./target/app` would set the `debug` key
            .merge(config::Environment::with_prefix("APP"))
            .unwrap();

        settings.try_into::<Config>().unwrap()
    }
}
