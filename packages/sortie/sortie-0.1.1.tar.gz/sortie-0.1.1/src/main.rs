use colored::Colorize;
use std::env;
use std::fs::{read_to_string, write};
use std::path::Path;
use std::process;
use taplo::{formatter, parser};
use taplo_common::config::Config;
use toml;
use toml::Table;

fn main() -> Result<(), &'static str> {
    let args: Vec<String> = env::args().collect();
    let is_check = parse_args_is_check(&args);
    let path = Path::new("pyproject.toml");
    let source = read_to_string(path).unwrap();
    // let pyproject_config: toml::Value = toml::from_str(&source).unwrap();
    let pyproject_config: Table = toml::from_str(&source).unwrap();
    let p = parser::parse(&source);

    let error_ranges = p.errors.iter().map(|e| e.range).collect::<Vec<_>>();
    let dom = p.into_dom();

    // set opinionated defaults
    let format_opts = get_format_options(&pyproject_config);

    let config = Config::default();

    let formatted = formatter::format_with_path_scopes(
        dom,
        format_opts,
        &error_ranges,
        config.format_scopes(&path),
    )
    .unwrap();
    if source != formatted {
        if is_check {
            eprintln!(
                "{}",
                format!("{}", "pyproject.toml would be formatted!".yellow())
            );
            process::exit(1);
        } else {
            match write(path, formatted) {
                Ok(_) => println!("pyproject.toml reformatted."),
                Err(err) => {
                    eprintln!(
                        "{} issue writing to pyproject.toml: {}",
                        "error:".red(),
                        err
                    );
                    process::exit(1);
                }
            }
        }
    } else if !is_check {
        println!("pyproject.toml left unchanged.")
    }
    Ok(())
}

fn parse_args_is_check(args: &[String]) -> bool {
    match &args[..] {
        [_] => false,
        [_, a] if a == "--check" => true,
        [_, a] => {
            eprintln!(
                "{} unexpected argument {} found!",
                "error:".red(),
                format!("'{}'", a).yellow()
            );
            process::exit(1);
        }
        _ => {
            eprintln!(
                "{} cmdline args only accepts {} or no arguments",
                "error:".red(),
                "'--check'".yellow()
            );
            process::exit(1);
        }
    }
}

fn get_format_options(pyproject_config: &Table) -> formatter::Options {
    let mut format_opts = formatter::Options::default();
    format_opts.reorder_keys =
        get_bool_option(pyproject_config, "reorder_keys", format_opts.reorder_keys);
    format_opts.reorder_arrays = get_bool_option(
        pyproject_config,
        "reorder_arrays",
        format_opts.reorder_arrays,
    );
    format_opts.align_entries =
        get_bool_option(pyproject_config, "align_entries", format_opts.align_entries);
    format_opts.align_comments = get_bool_option(
        pyproject_config,
        "align_comments",
        format_opts.align_comments,
    );
    format_opts.align_single_comments = get_bool_option(
        pyproject_config,
        "align_single_comments",
        format_opts.align_single_comments,
    );
    format_opts.array_trailing_comma = get_bool_option(
        pyproject_config,
        "array_trailing_comma",
        format_opts.array_trailing_comma,
    );
    format_opts.array_auto_expand = get_bool_option(
        pyproject_config,
        "array_auto_expand",
        format_opts.array_auto_expand,
    );
    format_opts.inline_table_expand = get_bool_option(
        pyproject_config,
        "inline_table_expand",
        format_opts.inline_table_expand,
    );
    format_opts.array_auto_collapse = get_bool_option(
        pyproject_config,
        "array_auto_collapse",
        format_opts.array_auto_collapse,
    );
    format_opts.compact_arrays = get_bool_option(
        pyproject_config,
        "compact_arrays",
        format_opts.compact_arrays,
    );
    format_opts.compact_inline_tables = get_bool_option(
        pyproject_config,
        "compact_inline_tables",
        format_opts.compact_inline_tables,
    );
    format_opts.compact_entries = get_bool_option(
        pyproject_config,
        "compact_entries",
        format_opts.compact_entries,
    );
    format_opts.indent_tables =
        get_bool_option(pyproject_config, "indent_tables", format_opts.indent_tables);
    format_opts.indent_entries = get_bool_option(
        pyproject_config,
        "indent_entries",
        format_opts.indent_entries,
    );
    format_opts.indent_string = get_string_option(
        pyproject_config,
        "indent_string",
        &format_opts.indent_string,
    );
    format_opts.trailing_newline = get_bool_option(
        pyproject_config,
        "trailing_newline",
        format_opts.trailing_newline,
    );
    format_opts.allowed_blank_lines = get_usize_option(
        pyproject_config,
        "allowed_blank_lines",
        format_opts.allowed_blank_lines as i64,
    ) as usize;
    format_opts.column_width = get_usize_option(
        pyproject_config,
        "column_width",
        format_opts.column_width as i64,
    ) as usize;
    format_opts.crlf = get_bool_option(pyproject_config, "crlf", format_opts.crlf);
    format_opts
}

fn get_bool_option(pyproject_config: &Table, key: &str, default: bool) -> bool {
    if let Some(tool_table) = pyproject_config.get("tool") {
        if let Some(sortie_table) = tool_table.get("sortie") {
            if let Some(value) = sortie_table.get(key) {
                return value.as_bool().unwrap_or(default);
            }
        }
    }
    default
}

fn get_string_option(pyproject_config: &Table, key: &str, default: &str) -> String {
    if let Some(tool_table) = pyproject_config.get("tool") {
        if let Some(sortie_table) = tool_table.get("sortie") {
            if let Some(value) = sortie_table.get(key) {
                return value.as_str().unwrap_or(default).to_string();
            }
        }
    }
    default.to_string()
}

fn get_usize_option(pyproject_config: &Table, key: &str, default: i64) -> i64 {
    if let Some(tool_table) = pyproject_config.get("tool") {
        if let Some(sortie_table) = tool_table.get("sortie") {
            if let Some(value) = sortie_table.get(key) {
                return value.as_integer().unwrap_or(default);
            }
        }
    }
    default
}
